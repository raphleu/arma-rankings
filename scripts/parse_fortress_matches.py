import json

score_limit = 200
matchtype = 'pickup-fortress1'
filename = matchtype + '.txt'
match_results = []
with open('raw_data/' + filename, 'r') as f:
    in_a_match_result = 0
    in_a_round_start = 0
    inferred_teams = {}
    for line in f:
        stripped_line = line.strip().split()

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
                if (team not in match_data['teams']): 
                    match_data['teams'][team] = {}
                    match_data['teams'][team]['players'] = []
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
                    registered_players = [pl['username'] for pl in match_data['teams'][team]['players']]
                    for player in inferred_teams[team]:
                        if player not in registered_players:
                            match_data['teams'][team]['players'].append({
                                'username': player,
                                'score': -1
                            })
                match_results.append(match_data)
            in_a_match_result = 0


with open('raw_data/' + matchtype + '_parsed.json', 'w') as fp:
    json.dump(match_results, fp)