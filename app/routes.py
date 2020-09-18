from app import app
from app.models import Elorating, Trueskillrating, Match, MatchScore
from datetime import date, datetime, timedelta
from flask import render_template, request
from google.cloud import secretmanager
import os
from sqlalchemy.orm import joinedload


schedule_for_us = [
    {
        'day': 'Thursdays',
        'time': [
            '00:00 GMT',
            '2:00 am CEST',
            '1:00 am BST',
            '8:00 pm EDT',
            '5:00 am PDT',
            '10:00 am AEST'
        ]
    },
    {
        'day': 'Saturdays',
        'time': [
            '21:00 GMT',
            '11:00 pm CEST',
            '10:00 pm BST',
            '5:00 pm EDT',
            '2:00 pm PDT',
            '7:00 am AEST'
        ]
    },
]

schedule_for_eu = [
    {
        'day': 'Tuesdays',
        'time': [
            '19:00 GMT',
            '9:00 pm CEST',
            '8:00 pm BST',
            '3:00 pm EDT',
            '12:00 pm PDT',
            '5:00 am AEST'
        ]
    },
    {
        'day': 'Saturdays',
        'time': [
            '18:00 GMT',
            '8:00 pm CEST',
            '7:00 pm BST',
            '2:00 pm EDT',
            '11:00 am PDT',
            '4:00 am AEST'
        ]
    },
]

sbl_eu_matchtype = 'sbl-eu'
sbl_us_matchtype = 'sbl-us'

match_types = {
    'sbl-us': {
        'header': 'US',
        'title': 'Sumo Bar League US',
        'matchtype': sbl_us_matchtype,
        'description': 'Public, ranked sumobar matches, hosted on US servers! Open to anyone, see <a href="/league-info">League Info</a> for how to join. Can you make it to the top?',
        'banner_image': 'titan_banner3.png'
    },
    'sbl-eu': {
        'header': 'EU',
        'title': 'Sumo Bar League EU',
        'matchtype': sbl_eu_matchtype,
        'description': 'Public, ranked sumobar matches, hosted on EU servers! Open to anyone, see <a href="/league-info">League Info</a> for how to join. Can you make it to the top?',
        'banner_image': 'titan_banner1.png'
    }
}

RATING_TYPE = 'elo'
if (os.getenv('RATING_TYPE')):
    RATING_TYPE = os.getenv('RATING_TYPE')

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        match_types=match_types,
        year=date.today().year
    )

@app.route('/rankings')
def league_rankings():
    match_type = request.args.get('matchtype', '')

    rankings = Trueskillrating.query.filter_by(matchtype=match_type).order_by(Trueskillrating.rating.desc()).all()

    return render_template(
        'rankings.html',
        rankings=rankings,
        matchtype=match_type,
        match_type= match_types[match_type],
        match_types=match_types,
        year=date.today().year
    )

@app.route('/league-info')
def league_info():
    return render_template(
        'league-info.html', 
        schedule_for_eu = {
            'days': schedule_for_eu
        },
        schedule_for_us = {
            'days': schedule_for_us
        },
        year=date.today().year,
        title='Sumo Bar League'
    )

@app.route('/matches')
def matches():
    matchtype = request.args.get('matchtype', '')
    two_weeks_ago = datetime.now() - timedelta(days=14)
    matches = Match.query.join(MatchScore).filter(Match.matchtype == matchtype).filter(Match.date >= two_weeks_ago).order_by(Match.date.desc())
    # I shouldn't need eager load, but if I do the query below should work. 
    # matches = Match.query.options(joinedload('match_scores')).filter(Match.matchtype == matchtype).order_by(Match.date.desc())

    return render_template(
        'matches.html',
        matches = matches,
        matchtype = matchtype.replace("-", " ").upper(),
        year=date.today().year
    )

@app.route('/matches/update')
def updateMatches():
    client = secretmanager.SecretManagerServiceClient()
    key = request.args.get('key', '')
    actual_key= client.access_secret_version('projects/794715043730/secrets/MATCH_ADMIN_KEY/versions/latest').payload.data
    if (key == actual_key):
        execfile("scripts/import_data.py")
        execfile("scripts/rank_trueskill.py")
        return "stuff"
    else:
        return "not stuff"