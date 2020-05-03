from flask import render_template
from app import app
from app.models import Elorating
from datetime import date


schedule_for_us = [
    {
        'day': 'Thursdays',
        'time_gmt': '00 GMT',
        'time_cest': '2am CEST',
        'time_bst': '1am BST',
        'time_edt': '11am EDT',
        'time_pdt': '8am PDT',
        'time_aest': '1am AEST'
    },
    {
        'day': 'Saturdays',
        'time_gmt': '21 GMT',
        'time_cest': '11pm CEST',
        'time_bst': '10pm BST',
        'time_edt': '5pm EDT',
        'time_pdt': '2pm PDT',
        'time_aest': '7am AEST'
    },
]

schedule_for_eu = [
    {
        'day': 'Tuesdays',
        'time_gmt': '19 GMT',
        'time_cest': '9pm CEST',
        'time_bst': '8pm BST',
        'time_edt': '3pm EDT',
        'time_pdt': 'noon PDT',
        'time_aest': '5am AEST'
    },
    {
        'day': 'Saturdays',
        'time_gmt': '15 GMT',
        'time_cest': '5pm CEST',
        'time_bst': '4pm BST',
        'time_edt': '11am EDT',
        'time_pdt': '8am PDT',
        'time_aest': '1am AEST'
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
