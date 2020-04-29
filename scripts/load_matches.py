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
                        rating = username_to_rating[username]
                        formatted_match.append(EloPlayer(place=place, elo=rating))
                    else:
                        formatted_match.append(EloPlayer(place=place, elo=starting_rating))
                    place += 1 
                ratings = calc_elo(formatted_match, k_factor)
                for i in range(len(ratings)):
                    username_to_rating[usernames[i]] = ratings[i]

        # print("Match count: " + str(match_count))

        # print("Matchtype: " + match_type)
        counter = 1
        for key in sorted(username_to_rating, key = lambda username: username_to_rating[username], reverse = True):
            # print(str(counter) + ". " + key + ": " + str(username_to_rating[key]))
            user = User(username=key)
            elorating = Elorating(username = key, matchtype = match_type, rating = username_to_rating[key])
            db.session.add(user)
            db.session.add(elorating)
            counter += 1

# commit all of our db changes
db.session.commit()