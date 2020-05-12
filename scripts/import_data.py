import gspread
import json
import sys
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name('armarankings-37612da47ced.json', scope)
    client = gspread.authorize(creds)
except:
    print "Unable to get credentials or authenticate with google drive. Not pulling match data from excel."
    sys.exit()

sheet = client.open("SBL-results")

worksheets = ["sbl-us-matches", "sbl-eu-matches"]

for worksheet in worksheets: 
    ws = sheet.worksheet(worksheet)
    list_of_rows = ws.get_all_values()
    match = {}
    matches = []
    for row in list_of_rows:
        if (row[0] == 'match'):
            if (bool(match)):
                matches.append(match)
            match = {
                'name': row[1],
                'matchtype': worksheet,
                'date': row[2],
                'match_scores': []
            }
        else:
            username = row[0]
            score = row[1]
            user_object = {
                'username': username,
                'score': score
            }
            match['match_scores'].append(user_object)

    matches.append(match)

    filepath = '../raw_data/' + worksheet + '_parsed.json'
    with open(filepath, 'w') as fp:
        json.dump(matches, fp)
