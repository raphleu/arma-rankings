import gspread
import json
import sys
from google.cloud import secretmanager
import os
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
try:
    flask_env = 'dev'
    if (os.getenv('FLASK_ENV')):
        flask_env = os.getenv('FLASK_ENV')

    if (flask_env == 'cloud'): # get spreadsheet credentials from a secret in google cloud
        client = secretmanager.SecretManagerServiceClient()
        creds_secret = json.loads(client.access_secret_version('projects/794715043730/secrets/SCORE_SHEET_CREDS/versions/latest').payload.data)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_secret)
    else:  # get spreadsheet credentials from a local file
        creds = ServiceAccountCredentials.from_json_keyfile_name('armarankings-37612da47ced.json', scope)
        
    client = gspread.authorize(creds)
except:
    print "Unable to get credentials or authenticate with google drive. Not pulling match data from excel."
    sys.exit()

sheet = client.open("SBL-results")

worksheets = ["sbl-us", "sbl-eu", "sbl-s2"]

for worksheet in worksheets: 
    print("Importing data from worksheet: " + worksheet)
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
            username = username.strip()
            score = row[1]
            user_object = {
                'username': username,
                'score': score
            }
            match['match_scores'].append(user_object)

    matches.append(match)

    filepath = '/home/ranking_app/raw_data/' + worksheet + '_parsed.json'
    with open(filepath, 'w') as fp:
        json.dump(matches, fp)
