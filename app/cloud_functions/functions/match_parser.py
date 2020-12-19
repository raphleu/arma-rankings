# A function to parse ladderlog files into a reasonable json format so we can 
# do some processing on the data. Currently works for: fort, tst
#
# log_string: a python string representation of a ladderlog.txt file
# score_limit: score limit for a match of this type
# matchtype: string identifier for this type of match. Whatever you want it to be
#
# returns: an array of python dictionary containing match information such as scores for
#   each match in the log_string passed in. I.e: 
# [
#     {
#         'name': "[matchtype].2020-08-14.19:22:56", 
#         'match_winner': 'team_orange',
#         'teams': {
#             'team_gold': {
#                 'players': [
#                     {
#                         'username': 'player@forums',
#                         'score': '510'    
#                     }, 
#                     ...
#                 ], 
#                 'score': '1725'
#             }, 
#             ...
#         }, 
#         'time': '19:22:56',
#         'date': '2020-08-14', 
#         'matchtype': [matchtype]
#     }
# ]
def parse_match_log(log_string, score_limit, matchtype):
    score_limit = score_limit
    matchtype = matchtype
    match_results = []
    in_a_match_result = 0
    in_a_round_start = 0
    inferred_teams = {}
    for line in log_string.splitlines():
        stripped_line = line.strip().split()
        if (len(stripped_line) < 1):
            continue
         # keeping track of who was playing at the start of the round incase people leave before the match officially ends
        if (stripped_line[0] == 'ROUND_ENDED'):
            inferred_teams = {}
            in_a_round_start = 1
        if (stripped_line[0] == 'ROUND_SCORE'):
            if (in_a_round_start):
                if (len(stripped_line) > 3):
                    username = stripped_line[2]
                    team = stripped_line[3]
                    if (team not in inferred_teams):
                        inferred_teams[team] = []
                    inferred_teams[team].append(username)
        if (stripped_line[0] == 'ROUND_SCORE_TEAM'):
            in_a_round_start = 0
        if (stripped_line[0] == 'MATCH_WINNER'):
            match_data = {}
            in_a_match_result = 1
            winning_team = stripped_line[1]
            match_data['match_winner'] = winning_team
            match_data['teams'] = {}
        if (stripped_line[0] == 'MATCH_SCORE' and in_a_match_result == 1):
            # if there's less than 3 elements, there's probably not a team name, meaning this was a spectator score
            if (len(stripped_line) > 3):
                team = stripped_line[3]
                username = stripped_line[2]
                score = stripped_line[1]
                player_dict = {
                    'username': username,
                    'score': score
                }
                print(match_data)
                if (team not in match_data['teams']): 
                    match_data['teams'][team] = {}
                    match_data['teams'][team]['players'] = []
                print(match_data)
                print(stripped_line)
                match_data['teams'][team]['players'].insert(0, player_dict)
        if (stripped_line[0] == 'MATCH_SCORE_TEAM'):
            team = stripped_line[2]
            score = stripped_line[1]
            if (team not in match_data['teams']): 
                match_data['teams'][team] = {}
            match_data['teams'][team]['score'] = score
        if (stripped_line[0] == 'MATCH_ENDED'):
            date = stripped_line[1]
            time = stripped_line[2]
            match_data['date'] = date
            match_data['time'] = time
            match_data['matchtype'] = matchtype
            match_data['name'] = matchtype + '.' + date + '.' + time
            # only count a match if there was a score over 200. This means it wasn't a random restart or something
            valid_match = False
            teams = match_data['teams']
            for team in teams:
                if (int(teams[team]['score']) >= score_limit):
                    valid_match = True
            if (valid_match):
                for team in inferred_teams:
                    registered_players = []
                    if (team in match_data['teams']):
                        if ('players' in match_data['teams'][team]):
                            registered_players = [pl['username'] for pl in match_data['teams'][team]['players']]
                    # All players from this team left before the match actually ended, so MATCH_SCORE_TEAM wasn't printed for them
                    else:
                        match_data['teams'][team] = {
                            'players': [],
                            'score': '-1'
                        }
                        registered_players = []
                    for player in inferred_teams[team]:
                        if player not in registered_players:
                            if ('players' in match_data['teams'][team]): 
                                match_data['teams'][team]['players'].append({
                                    'username': player,
                                    'score': '-1'
                                })
                            else:
                                match_data['teams'][team]['players'] = [{
                                    'username': player,
                                    'score': '-1'
                                }]
                match_results.append(match_data)
            in_a_match_result = 0
    return match_results