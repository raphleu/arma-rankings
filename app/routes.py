from flask import render_template
from app import app
from app.models import Elorating


@app.route('/')
@app.route('/index')
def index():
    eu_rankings = Elorating.query.filter_by(matchtype='sbl_eu_scorelog').order_by(Elorating.rating.desc()).all()
    us_rankings = Elorating.query.filter_by(matchtype='sbl_us_scorelog').order_by(Elorating.rating.desc()).all()
    countries = [
        {
            'header': 'US',
            'ranking': us_rankings,
            'days': [
                {
                'day': 'Thursdays',
                'time_gmt': '00 GMT',
                'time_est': '8pm EST',
                },
                {
                    'day': 'Saturdays',
                    'time_gmt': '21 GMT',
                    'time_est': '5pm EST',
                },
            ]
        },
        {
            'header': 'EU',
            'ranking': eu_rankings,
            'days': [
                {
                    'day': 'Tuesdays',
                    'time_gmt': '19 GMT',
                    'time_est': '9pm EST',
                },
                {
                    'day': 'Saturdays',
                    'time_gmt': '15 GMT',
                    'time_est': '5pm EST',
                },
            ]
        }
    ]

    return render_template(
        'index.html',
        title='Sumobar League',
        countries=countries
    )


@app.route('/league_info')
def league_info():
    return render_template('league_info.html')
