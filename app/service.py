from app import app, db
from app.models import Elorating, Trueskillrating, Match, MatchScore
import random
from sqlalchemy import func

# This should be in a service layer somewhere instead of here. 
#
# Here are some play lists I used for test cases:
# players = ["raph123@forums", "Ampz@forums", "vov@forums", "misterplayer@forums", "Desolate@forums", "veinxat@forums", "garlic@forums", "Soul@forums", "Fini@forums", "Moonlight@forums"]
# all c tier
# players = ["Player51@forums", "eezeez@forums", "beitzer@lt", "Soul@forums", "NoahFence@forums", "TattooOG@forums", "garlic@forums", "naiss@forums", "ClundXIII@forums", "Smurf@forums"]
# with 4 non c tier (should always choose non c tier captains)
# players = ["raph123@forums", "Ampz@forums", "vov@forums", "misterplayer@forums", "NoahFence@forums", "TattooOG@forums", "garlic@forums", "naiss@forums", "ClundXIII@forums", "Smurf@forums"]
# with weird casing
# players = ["Raph123@forums", "ampz@forums", "vov@forums", "misterplayer@forums", "NoahFence@forums", "TattooOG@forums", "garlic@forums", "naiss@forums", "ClundXIII@forums", "Smurf@forums"]
def generateTeamsService(players):
    if (len(players) < 2): 
        return { 
            'error': 'Too few players signed up.'
        }

    # Get the "percent rank" for each player passed in
    subquery = db.session.query(
        Trueskillrating.username,
        func.percent_rank().over(
            order_by=Trueskillrating.rating.desc()
        ).label('pct-rnk'),
    ).filter_by(matchtype='pickup-fortress1').subquery()
    query = db.session.query(subquery).filter(
        func.lower(subquery.c.username).in_([p.lower() for p in players])
    )
    percent_ranked_ratings = query.all()

    s_tiers, a_tiers, b_tiers, c_tiers = ([] for i in range(4))

    s_tier = .1 # top 10% of rankings
    a_tier = .25 # 10-25%
    b_tier = .6 # 25-60%
    c_tier = 1 # 60-100

    # Shuffle the players so that players within a tier are in a random order. We will sort by tier next.
    random.shuffle(percent_ranked_ratings)

    for rating in percent_ranked_ratings:
        percent_rank = rating[1]
        if (percent_rank <= s_tier):
            s_tiers.append(rating)
        elif (percent_rank <= a_tier):
            a_tiers.append(rating)
        elif (percent_rank <= b_tier):
            b_tiers.append(rating)
        elif (percent_rank <= c_tier):
            c_tiers.append(rating)
    
    # Separate s, a, and b tier players for selecting captain, if we have enough from those tiers. 
    semi_sorted_ratings_sab = s_tiers + a_tiers + b_tiers
    semi_sorted_ratings_all = s_tiers + a_tiers + b_tiers + c_tiers

    # If we have enough players in s, a and b tiers, randomly choose captains from there
    if (len(semi_sorted_ratings_sab) > 3):
        captain_1_index = random.randrange(0, len(semi_sorted_ratings_sab) - 1, 2)
        captain_2_index = captain_1_index + 1
        captain_2 = semi_sorted_ratings_sab[captain_2_index].username
        captain_1 = semi_sorted_ratings_sab[captain_1_index].username
    else: 
        captain_1_index = random.randrange(0, len(semi_sorted_ratings_all) - 1, 2)
        captain_2_index = captain_1_index + 1
        captain_2 = semi_sorted_ratings_all[captain_2_index].username
        captain_1 = semi_sorted_ratings_all[captain_1_index].username

    team_2 = []
    team_1 = []
    counter = 2

    # Assign players to teams using abbaabb... approach.
    while (len(semi_sorted_ratings_all) > 0):
        if (counter <= 2):
            team_2.append(semi_sorted_ratings_all.pop(0).username)
        elif (counter <= 4):
            team_1.append(semi_sorted_ratings_all.pop(0).username)
        elif (counter == 5):
            counter = 0
        counter += 1

    # Figure out which team our captians are in since we assigned teams after choosing captains.
    if captain_1 in team_1:
        team_1_captain = captain_1
        team_2_captain = captain_2
    else:
        team_1_captain = captain_2
        team_2_captain = captain_1

    return {
        'team_1': {
            'captain': team_1_captain,
            'players': team_1
        },
        'team_2': {
            'captain': team_2_captain,
            'players': team_2
        }
    }