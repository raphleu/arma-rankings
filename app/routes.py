from flask import render_template
from app import app
from app.models import Elorating 

@app.route('/')
@app.route('/index')
def index():
    eu_rankings = Elorating.query.filter_by(matchtype='sbl_eu_scorelog').order_by(Elorating.rating.desc()).all()
    us_rankings = Elorating.query.filter_by(matchtype='sbl_us_scorelog').order_by(Elorating.rating.desc()).all()

    return render_template('index.html', title = 'Sumobar League', us_rankings = us_rankings, eu_rankings = eu_rankings)