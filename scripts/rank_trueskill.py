import datetime
import json
import operator
from trueskill import Rating, TrueSkill
from os import sys, path, listdir

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from app import db
from app.models import User, Trueskillrating, Match, MatchScore

fort_env = TrueSkill(mu=8, sigma=3, draw_probability=0.0, beta=7, tau=0.07)
fort_env.make_as_global()

env = TrueSkill()

# clear existing ratings from the DB
User.query.delete()
Trueskillrating.query.delete()
MatchScore.query.delete()
Match.query.delete()

base_rating = 1500
multiplier = 23.45

match_type = ''
directory_to_scan = '/home/ranking_app/raw_data'
for filename in listdir(directory_to_scan):
    with open(directory_to_scan + '/' + filename) as f:
        if ('.txt' in filename):
            # do nothing
            print('This is a .txt file. Carrying on.')
            continue
        elif ('pickup-fortress' in filename):
            print('Ranking: ' + filename)
            matches = json.load(f)
            username_to_rating = {}
            match_count = 0
            for match in matches:
                match_type = match['matchtype']
                match_date_obj = datetime.datetime.strptime(match['date'], "%Y-%m-%d")
                match_data = Match(
                    name = match['name'],
                    matchtype = match_type,
                    date = match_date_obj
                )
                db.session.add(match_data)
                db.session.flush() # This will give us an ID for the match that has not yet been commited
                match_count += 1
                formatted_match = []
                match_teams = match['teams']
                sorted_teams = sorted(match_teams, key = lambda x: (match_teams[x]['score']), reverse=True)
                place = 1
                for team in sorted_teams:
                    team_rankings = {}
                    for player in match_teams[team]['players']:
                        username = player['username']
                        username = username.replace("\_"," ")
                        if (username_to_rating.has_key(username)):
                            rating = username_to_rating[username]['rating']
                            team_rankings[username] = rating
                        else:
                            rating = Rating(mu=4)
                            team_rankings[username] = rating
                        transformed_rating = round((rating.mu - 3 * rating.sigma) * multiplier + base_rating, 0)
                        match_score = MatchScore(
                            match_id = match_data.id,
                            username = username,
                            score = player['score'],
                            place = place,
                            entry_rating = transformed_rating,
                        )
                        db.session.add(match_score)
                    formatted_match.append(team_rankings)
                    place += 1
                match_data.quality = round(fort_env.quality(formatted_match), 4)
                teams_ratings = fort_env.rate(formatted_match)
                for team_ratings in teams_ratings:
                    for username, rating in team_ratings.items(): 
                        old_rating = 1500
                        if (username_to_rating.has_key(username)):
                            old_rating = username_to_rating[username]['rating'].mu - 3 * username_to_rating[username]['rating'].sigma
                            old_rating = old_rating * multiplier + base_rating
                        new_rating = rating.mu - 3 * rating.sigma
                        new_rating = new_rating * multiplier + base_rating
                        rating_data = {}
                        rating_data['latest_delta'] = round(new_rating, 0) - round(old_rating, 0)
                        rating_data['latest_delta_date'] = match_date_obj
                        rating_data['rating'] = rating 
                        username_to_rating[username] = rating_data
        else: 
            print('Ranking: ' + filename)
            matches = json.load(f)
            username_to_rating = {}
            match_count = 0
            for match in matches:
                if (len(match['match_scores']) > 1):
                    match_type = match['matchtype']
                    match_date_obj = datetime.datetime.strptime(match['date'], "%Y-%m-%d")
                    match_data = Match(
                        name = match['name'],
                        matchtype = match_type,
                        date = match_date_obj
                    )
                    db.session.add(match_data)
                    db.session.flush() # This will give us an ID for the match that has not yet been commited
                    match_count += 1
                    formatted_match = []
                    place = 1
                    for player in match['match_scores']:
                        username = player['username']
                        if (username_to_rating.has_key(username)):
                            rating = username_to_rating[username]['rating']
                            formatted_match.append({username: rating})
                        else:
                            rating = Rating()
                            formatted_match.append({username: rating})
                        match_score = MatchScore(
                            match_id = match_data.id,
                            username = username,
                            score = player['score'],
                            place = place,
                        )
                        db.session.add(match_score)
                        place += 1 

                    match_data.quality = round(env.quality(formatted_match), 4)
                    ratings = env.rate(formatted_match)
                    for rating in ratings:
                        for username, rating in rating.items(): 
                            old_rating = 1500
                            if (username_to_rating.has_key(username)):
                                old_rating = username_to_rating[username]['rating'].mu - 3 * username_to_rating[username]['rating'].sigma
                                old_rating = old_rating * multiplier + base_rating
                            new_rating = rating.mu - 3 * rating.sigma
                            new_rating = new_rating * multiplier + base_rating
                            rating_data = {}
                            rating_data['latest_delta'] = round(new_rating, 0) - round(old_rating, 0)
                            rating_data['latest_delta_date'] = match_date_obj
                            rating_data['rating'] = rating 
                            username_to_rating[username] = rating_data

# print("Match count: " + str(match_count))
# 
# counter = 1
# for key in sorted(username_to_rating, key = lambda username: username_to_rating[username].mu, reverse = True):
#     print(str(counter) + ". " + key + ": " + str(username_to_rating[key].mu-(3*username_to_rating[key].sigma)) + ", " + str(username_to_rating[key].mu) + ", " + str(username_to_rating[key].sigma))
#     counter += 1


        for key in username_to_rating:
            user = User(username=key)
            rating = username_to_rating[key]['rating'].mu - 3*username_to_rating[key]['rating'].sigma
            rating = rating * multiplier + base_rating
            trueskillrating = Trueskillrating(
                username = key,
                matchtype = match_type,
                mu = round(username_to_rating[key]['rating'].mu, 2),
                sigma = round(username_to_rating[key]['rating'].sigma, 2),
                rating = round(rating, 0),
                latest_delta = username_to_rating[key]['latest_delta'],
                latest_delta_date = username_to_rating[key]['latest_delta_date']
            )
            db.session.add(user)
            db.session.add(trueskillrating)

db.session.commit()
