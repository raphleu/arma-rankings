from flask import render_template
from app import app
from app.models import Elorating
from datetime import date


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
            '15:00 GMT',
            '5:00 pm CEST',
            '4:00 pm BST',
            '11:00 am EDT',
            '8:00 am PDT',
            '1:00 am AEST'
        ]
    },
]

@app.route('/')
@app.route('/index')
def index():
    eu_rankings = Elorating.query.filter_by(matchtype='sbl-eu-matches').order_by(Elorating.rating.desc()).all()
    us_rankings = Elorating.query.filter_by(matchtype='sbl-us-matches').order_by(Elorating.rating.desc()).all()
    countries = [
        {
            'header': 'US',
            'ranking': us_rankings
        },
        {
            'header': 'EU',
            'ranking': eu_rankings
        }
    ]

    return render_template(
        'index.html',
        title='Sumo Bar League',
        countries=countries,
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
    return render_template(
        'matches.html'
    )