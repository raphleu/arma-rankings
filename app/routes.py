from flask import render_template
from app import app
from app.models import Elorating
from datetime import date


schedule_for_us = [
    {
        'day': 'Thursdays',
        'time': [
            '00 GMT',
            '2am CEST',
            '1am BST',
            '11am EDT',
            '8am PDT',
            '1am AEST'
        ]
    },
    {
        'day': 'Saturdays',
        'time': [
            '21 GMT',
            '11pm CEST',
            '10pm BST',
            '5pm EDT',
            '2pm PDT',
            '7am AEST'
        ]
    },
]

schedule_for_eu = [
    {
        'day': 'Tuesdays',
        'time': [
            '19 GMT',
            '9pm CEST',
            '8pm BST',
            '3pm EDT',
            'noon PDT',
            '5am AEST'
        ]
    },
    {
        'day': 'Saturdays',
        'time': [
            '15 GMT',
            '5pm CEST',
            '4pm BST',
            '11am EDT',
            '8am PDT',
            '1am AEST'
        ]
    },
]

@app.route('/')
@app.route('/index')
def index():
    eu_rankings = Elorating.query.filter_by(matchtype='sbl_eu_scorelog').order_by(Elorating.rating.desc()).all()
    us_rankings = Elorating.query.filter_by(matchtype='sbl_us_scorelog').order_by(Elorating.rating.desc()).all()
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
