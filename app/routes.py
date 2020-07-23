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

RATING_TYPE = 'elo'
if (os.getenv('RATING_TYPE')):
    RATING_TYPE = os.getenv('RATING_TYPE')

@app.route('/')
@app.route('/index')
def index():
    sbl_eu_matchtype = 'sbl-eu'
    sbl_us_matchtype = 'sbl-us'

    if (RATING_TYPE == 'trueskill'):
        eu_rankings = Trueskillrating.query.filter_by(matchtype=sbl_eu_matchtype).order_by(Trueskillrating.rating.desc()).all()
        us_rankings = Trueskillrating.query.filter_by(matchtype=sbl_us_matchtype).order_by(Trueskillrating.rating.desc()).all()
    else:
        eu_rankings = Elorating.query.filter_by(matchtype=sbl_eu_matchtype).order_by(Elorating.rating.desc()).all()
        us_rankings = Elorating.query.filter_by(matchtype=sbl_us_matchtype).order_by(Elorating.rating.desc()).all()
    
    # for ranking in eu_rankings:
    #     ranking.latest_delta_date = datetime.

    match_types = [
        {
            'header': 'US',
            'ranking': us_rankings,
            'matchtype': sbl_us_matchtype
        },
        {
            'header': 'EU',
            'ranking': eu_rankings,
            'matchtype': sbl_eu_matchtype
        }
    ]

    return render_template(
        'index.html',
        title='Sumo Bar League',
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
        year=date.today().year
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