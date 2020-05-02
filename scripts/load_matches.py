import json
import operator
from multi_elo import EloPlayer, calc_elo
from os import sys, path, listdir

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from app import db
from app.models import User, Elorating

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
        match_type = filename.rstrip('_parsed.json')

        username_to_rating = {}

        match_count = 0
        for match in matches:
            if (len(match) > 1):
                match_count += 1
                formatted_match = []
                place = 1
                usernames = []
                for player in match:
                    username = player['username']
                    usernames.append(username)
                    if (username_to_rating.has_key(username)):
                        rating = username_to_rating[username]['rating']
                        formatted_match.append(EloPlayer(place=place, elo=rating))
                    else:
                        formatted_match.append(EloPlayer(place=place, elo=starting_rating))
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