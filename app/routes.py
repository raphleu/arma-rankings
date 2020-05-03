from flask import render_template
from app import app
from app.models import Elorating
from datetime import date


schedule_for_us = [
    {
        'day': 'Tuesdays',
        'time_gmt': '00 GMT',
        'time_est': '8pm EST',
    },
    {
        'day': 'Saturdays',
        'time_gmt': '21 GMT',
        'time_est': '5pm EST',
    },
]

schedule_for_eu = [
    {
        'day': 'Tuesdays',
        'time_gmt': '19 GMT',
        'time_est': '1pm EST',
    },
    {
        'day': 'Saturdays',
        'time_gmt': '15 GMT',
        'time_est': '11am EST',
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
        title='Sumobar League',
        countries=countries,
        year=date.today().year
    )


@app.route('/league_info')
def league_info():
    return render_template(
        'league_info.html', 
        schedule_for_eu = {
            'days': schedule_for_eu
        },
        schedule_for_us = {
            'days': schedule_for_us
        },
        year=date.today().year
    )
