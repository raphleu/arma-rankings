import datetime
import json
import operator
from multi_elo import EloPlayer, calc_elo
from os import sys, path, listdir

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from app import db
from app.models import User, Elorating, Match, MatchScore

k_factor = 32
starting_rating = 1500

# clear existing ratings from the DB
User.query.delete()
Elorating.query.delete()

match_type = ''
directory_to_scan = '../raw_data'
for filename in listdir('../raw_data'):
    with open('../raw_data/' + filename) as f:
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
                usernames = []
                for player in match['match_scores']:
                    username = player['username']
                    usernames.append(username)
                    if (username_to_rating.has_key(username)):
                        rating = username_to_rating[username]['rating']
                        formatted_match.append(EloPlayer(place=place, elo=rating))
                    else:
                        formatted_match.append(EloPlayer(place=place, elo=starting_rating))
                    match_score = MatchScore(
                        match_id = match_data.id,
                        username = player['username'],
                        score = player['score'],
                        place = place,
                    )
                    db.session.add(match_score)
                    place += 1 
                ratings = calc_elo(formatted_match, k_factor)
                for i in range(len(ratings)):
                    username = usernames[i]
                    old_rating = 1500
                    if (username_to_rating.has_key(username)): 
                        old_rating = username_to_rating[username]['rating']
                    new_rating = ratings[i]
                    rating_data = {}
                    rating_data['rating'] = new_rating
                    rating_data['latest_delta'] = new_rating - old_rating
                    username_to_rating[username] = rating_data


        # print("Match count: " + str(match_count))

        # The sorting below was for generating a nice printed list. Since everything is being stored to a db now, we don't need the sort (it will happen later)
        # Still going to leave the code in just in case it comes in handy at some point. 
        #  
        # print("Matchtype: " + match_type)
        # counter = 1
        # for key in sorted(username_to_rating, key = lambda username: username_to_rating[username], reverse = True):
            # print(str(counter) + ". " + key + ": " + str(username_to_rating[key]))
            # user = User(username=key)
            # elorating = Elorating(username = key, matchtype = match_type, rating = username_to_rating[key]['rating'], latest_delta = username_to_rating[key]['latest_delta'])
            # db.session.add(user)
            # db.session.add(elorating)
            # counter += 1

        for key in username_to_rating:
            user = User(username=key)
            elorating = Elorating(username = key, matchtype = match_type, rating = username_to_rating[key]['rating'], latest_delta = username_to_rating[key]['latest_delta'])
            db.session.add(user)
            db.session.add(elorating)

# commit all of our db changes
db.session.commit()