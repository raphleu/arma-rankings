import datetime
import json
import operator
from trueskill import Rating, TrueSkill
from os import sys, path, listdir

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from app import db
from app.models import User, Trueskillrating, Match, MatchScore
from app.app_config import live_seasons

base_addition = 1500
multiplier = 23.45

matches_to_exclude = {"pickup-tst1.2022-10-21.03:28:01"}

def transform_rating(mu, sigma):
    return round((mu - 3 * sigma) * multiplier + base_addition, 0)

def match_already_exists(match_name, match_type):
    matching_match_count = db.session.query(Match).filter(Match.name.like(match_name), Match.matchtype.like(match_type)).count()
    if (matching_match_count > 0):
        return True
    else:
        return False

def user_already_exists(username):
    matching_user_count = db.session.query(User).filter(User.username.like(username)).count()
    if (matching_user_count > 0):
        return True
    else:
        return False

def get_updated_ratings(match, match_date_obj, starting_mu, username_to_rating, match_type):
    match_teams = match['teams']
    sorted_teams = sorted(match_teams, key = lambda x: (int(match_teams[x]['score'])), reverse=True)
    match_data = Match(
        name = match['name'],
        matchtype = match_type,
        date = match_date_obj
    )
    db.session.add(match_data)
    db.session.flush() # This will give us an ID for the match that has not yet been commited
    place = 1
    match_scores = {}
    formatted_match = []
    for team in sorted_teams:
        team_rankings = {}
        if not 'players' in match_teams[team]:
            return None
            # print(match)
        for player in match_teams[team]['players']:
            username = player['username']
            username = username.replace("\_"," ")
            if (username_to_rating.has_key(username)):
                rating = username_to_rating[username]['rating']
                team_rankings[username] = rating
            else:
                rating = Rating(mu=starting_mu)
                team_rankings[username] = rating
            transformed_rating = transform_rating(rating.mu, rating.sigma)
            match_score = MatchScore(
                match_id = match_data.id,
                username = username,
                score = player['score'],
                place = place,
                entry_rating = transformed_rating,
            )
            db.session.add(match_score)
            match_scores[username] = match_score
        formatted_match.append(team_rankings)
        place += 1
    match_data.quality = round(env.quality(formatted_match), 4)
    teams_ratings = env.rate(formatted_match)
    for team_ratings in teams_ratings:
        for username, rating in team_ratings.items(): 
            old_rating = starting_rating
            if (username_to_rating.has_key(username)):
                old_rating = transform_rating(username_to_rating[username]['rating'].mu, username_to_rating[username]['rating'].sigma)
            new_rating = transform_rating(rating.mu, rating.sigma)
            match_scores[username].exit_rating = new_rating
            rating_data = {}
            rating_data['latest_delta'] = new_rating - old_rating
            rating_data['latest_delta_date'] = match_date_obj
            rating_data['rating'] = rating 
            username_to_rating[username] = rating_data
    return username_to_rating

def remove_existing_ratings(match_type):
    db.session.query(Trueskillrating).filter(Trueskillrating.matchtype == match_type).delete()
    # db.session.commit() # not sure if we need this here or if it can just be part of the later commit

def save_new_ratings(username_to_rating, match_type):
    for key in username_to_rating:
        if not (user_already_exists(key)):
            user = User(username=key)
            db.session.add(user)
        rating = transform_rating(username_to_rating[key]['rating'].mu, username_to_rating[key]['rating'].sigma)
        trueskillrating = Trueskillrating(
            username = key,
            matchtype = match_type,
            mu = round(username_to_rating[key]['rating'].mu, 2),
            sigma = round(username_to_rating[key]['rating'].sigma, 2),
            rating = rating,
            latest_delta = username_to_rating[key]['latest_delta'],
            latest_delta_date = username_to_rating[key]['latest_delta_date']
        )
        db.session.add(trueskillrating)

match_type = ''
directory_to_scan = '/home/ranking_app/raw_data'

for filename in listdir(directory_to_scan):
    with open(directory_to_scan + '/' + filename) as f:
        if ('.txt' in filename):
            # do nothing
            print('This is a .txt file. Carrying on.')
            continue
        print('Ranking: ' + filename)
        matches = json.load(f)
        username_to_rating = {}
        username_to_live_rating = {}

        pickup_fort_type = 0
        pickup_tst_type = 0

        starting_mu = 25.0
        sigma = 8.333333333333334
        if 'pickup-fortress' in filename: 
            pickup_fort_type = 1
            starting_mu = 4
            sigma = 3
            starting_rating = transform_rating(starting_mu,sigma)
            mu = 8
            env = TrueSkill(mu=starting_mu, sigma=sigma, draw_probability=0.0, beta=7, tau=0.07)
        if 'pickup-tst' in filename:
            pickup_tst_type = 1
            # using the default mu and sigma here
            starting_rating = transform_rating(mu=starting_mu, sigma=sigma)
            env = TrueSkill()
        else: 
            # using the default mu and sigma here
            starting_rating = transform_rating(mu=starting_mu, sigma=sigma)
            env = TrueSkill()
        env.make_as_global()

        if (pickup_fort_type or pickup_tst_type):
            for match in matches:
                match_type = match['matchtype']
                if match['name'] in matches_to_exclude:
                    print("Excluding match: " + match['name'])
                    continue
                # if this match already exists in the DB, we don't want to do anything with it, so we'll carry on to the next match
                if match_already_exists(match['name'], match_type):
                    print("Found a duplicate match with name: " + match['name'])
                    continue
                match_date_obj = datetime.datetime.strptime(match['date'], "%Y-%m-%d")
                username_to_rating_after = get_updated_ratings(match, match_date_obj, starting_mu, username_to_rating, match_type)
                if (username_to_rating_after is None):
                    continue
                else:
                    username_to_rating = username_to_rating_after
                if match_type in live_seasons:
                    if (datetime.datetime.today() - match_date_obj).days < 90:
                        username_to_live_rating = get_updated_ratings(match, match_date_obj, starting_mu, username_to_live_rating, match_type + "_live")
        else: 
            for match in matches:
                # if this match already exists in the DB, we don't want to do anything with it, so we'll carry on to the next match
                if match_already_exists(match['name'], match['matchtype']):
                    print("Found a duplicate match with name: " + match['name'])
                    continue
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
                    formatted_match = []
                    place = 1
                    match_scores = {}
                    for player in match['match_scores']:
                        username = player['username']
                        if (username_to_rating.has_key(username)):
                            rating = username_to_rating[username]['rating']
                            formatted_match.append({username: rating})
                        else:
                            rating = Rating()
                            formatted_match.append({username: rating})
                        transformed_rating = transform_rating(rating.mu, rating.sigma)
                        match_score = MatchScore(
                            match_id = match_data.id,
                            username = username,
                            score = player['score'],
                            place = place,
                            entry_rating = transformed_rating,
                        )
                        db.session.add(match_score)
                        match_scores[username] = match_score
                        place += 1 

                    match_data.quality = round(env.quality(formatted_match), 4)
                    ratings = env.rate(formatted_match)
                    for rating in ratings:
                        for username, rating in rating.items(): 
                            old_rating = starting_rating
                            if (username_to_rating.has_key(username)):
                                old_rating = transform_rating(username_to_rating[username]['rating'].mu, username_to_rating[username]['rating'].sigma)
                            new_rating = transform_rating(rating.mu, rating.sigma)
                            match_scores[username].exit_rating = new_rating
                            rating_data = {}
                            rating_data['latest_delta'] = new_rating - old_rating
                            rating_data['latest_delta_date'] = match_date_obj
                            rating_data['rating'] = rating 
                            username_to_rating[username] = rating_data
        remove_existing_ratings(match_type)
        save_new_ratings(username_to_rating, match_type)
        save_new_ratings(username_to_live_rating, match_type + "_live")
db.session.commit()
