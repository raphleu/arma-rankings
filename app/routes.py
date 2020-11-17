from app import app, db
from app.models import Elorating, Trueskillrating, Match, MatchScore
from datetime import date, datetime, timedelta
from flask import render_template, request, url_for
from google.cloud import secretmanager
import os
from sqlalchemy import func
from sqlalchemy.dialects.mssql import INTEGER
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import coalesce


schedule_for_us = [
    {
        'day': 'Thursdays',
        'utc_time': '00:00'
    },
    {
        'day': 'Saturdays',
        'utc_time': '21:00'
    },
]

schedule_for_eu = [
    {
        'day': 'Tuesdays',
        'utc_time': '19:00'
    },
    {
        'day': 'Saturdays',
        'utc_time': '19:00'
    },
]

match_types = {
    'leagues': {
        'sbl-s2': {
            'header': 'SBL',
            'title': 'Sumo Bar League',
            'match_subtype_id': 'sbl-s2',
            'description': 'Public, ranked sumobar matches, hosted on US and EU servers! Open to anyone, see <a href="/league-info?match_subtype_id=sbl-s2">League Info</a> for how to join. Can you make it to the top?',
            'banner_image': 'titan_banner2.png',
            'text_image': 'sbls2text.png'
        }
    },
    'pickup': {
        'pickup-fortress1': {
            'header': 'Fort',
            'title': 'Fortress pickup',
            'match_subtype_id': 'pickup-fortress1',
            'description': 'Pickup fortress! Competitive 6v6 gameplay. Sign up on discord in the #pickup channel!',
            'banner_image': 'fort_bg2.png',
            'text_image': 'fortpickuptext.png',
            'about': 'The ratings here are calculated using an algorithm called Trueskill, invented by microsoft for multiplayer games. Trueskill has many factors that go into it and can be tuned. For example, Trueskill takes into account the strength of your opposing team, so two players with the same number of wins and losses can have different ratings (a loss to a high rated team means less of a hit to your rating than one to a weaker team). Individual score does not matter, purely winning or losing and who you are against. More info can be found <a href="https://trueskill.org/">here</a>. I have tried tuning parameters to work best for this gametype, but if you have suggestions for how they can be improved, please let me (raph) know. <b>Play in 20 or more matches to show up in the rankings.'
        },
        'pickup-tst1': {
            'header': 'TST',
            'title': 'TST pickup',
            'match_subtype_id': 'pickup-tst1',
            'description': 'Pickup TST! Competitive 2v2v2v2 sumo gameplay. Sign up on discord in the #pickup channel!',
            'banner_image': 'titan_banner3.png',
            'text_image': 'tstpickuptext.png',
            'about': 'The ratings here are calculated using an algorithm called Trueskill, invented by microsoft for multiplayer games. Trueskill has many factors that go into it and can be tuned. For example, Trueskill takes into account the strength of your opposing team, so two players with the same number of wins and losses can have different ratings (a loss to a high rated team means less of a hit to your rating than one to a weaker team). Individual score does not matter, purely winning or losing and who you are against. More info can be found <a href="https://trueskill.org/">here</a>. I have tried tuning parameters to work best for this gametype, but if you have suggestions for how they can be improved, please let me (raph) know. <b>Play in 20 or more matches to show up in the rankings.'
        }
    },
    'archive': {
        'sbl-us': {
            'header': 'US',
            'title': 'Sumo Bar League US',
            'match_subtype_id': 'sbl-us',
            'description': 'Public, ranked sumobar matches, hosted on US servers! Open to anyone, see <a href="/league-info?match_subtype_id=sbl-us">League Info</a> for how to join. Can you make it to the top?',
            'banner_image': 'titan_banner3.png',
            'text_image': 'sumobarusatext.png'
        },
        'sbl-eu': {
            'header': 'EU',
            'title': 'Sumo Bar League EU',
            'match_subtype_id': 'sbl-eu',
            'description': 'Public, ranked sumobar matches, hosted on EU servers! Open to anyone, see <a href="/league-info?match_subtype_id=sbl-eu">League Info</a> for how to join. Can you make it to the top?',
            'banner_image': 'titan_banner1.png', 
            'text_image': 'sumobartexteu.png'
        }
    }
}

match_subtype_to_type = {
    'pickup-fortress1': 'pickup',
    'sbl-s2': 'leagues',
    'sbl-eu': 'archive',
    'sbl-us': 'archive',
    'pickup-tst1': 'pickup'
}

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
    match_subtype_id = request.args.get('match_subtype_id', '')
    match_type = match_subtype_to_type[match_subtype_id]

    matches_won_stmt = db.session.query(MatchScore.username, func.count('*').label('match_win_count')).filter(MatchScore.place == 1).join(Match).filter(Match.matchtype==match_subtype_id).group_by(MatchScore.username).subquery()
    matches_lost_stmt = db.session.query(MatchScore.username, func.count('*').label('match_lost_count')).filter(MatchScore.place > 1).join(Match).filter(Match.matchtype==match_subtype_id).group_by(MatchScore.username).subquery()
    average_score_stmt = db.session.query(MatchScore.username, func.cast(func.round(func.avg(MatchScore.score)), INTEGER).label('average_score')).filter(MatchScore.score > -1).join(Match).filter(Match.matchtype==match_subtype_id).group_by(MatchScore.username).subquery()

    rankings = db.session.query(Trueskillrating, coalesce(matches_won_stmt.c.match_win_count,0).label('match_win_count'), coalesce(matches_lost_stmt.c.match_lost_count,0).label('match_lost_count'), coalesce(average_score_stmt.c.average_score, 0).label('average_score'))\
        .filter_by(matchtype=match_subtype_id).filter(~Trueskillrating.username.contains('@L_OP'))\
        .outerjoin(matches_won_stmt, Trueskillrating.username==matches_won_stmt.c.username)\
        .outerjoin(matches_lost_stmt, Trueskillrating.username==matches_lost_stmt.c.username)\
        .outerjoin(average_score_stmt, Trueskillrating.username==average_score_stmt.c.username)

    if (match_type == 'pickup'):
        # A clause where you need 20 or more matches to show up
        rankings = rankings.filter(coalesce(matches_won_stmt.c.match_win_count,0) + coalesce(matches_lost_stmt.c.match_lost_count,0) >= 20)
   
    rankings = rankings.order_by(Trueskillrating.rating.desc()).all()

    return render_template(
        'rankings.html',
        rankings=rankings,
        match_type=match_type,
        match_subtype= match_types[match_type][match_subtype_id],
        match_types=match_types,
        year=date.today().year
    )

@app.route('/league-info')
def league_info():
    match_subtype_id = request.args.get('match_subtype_id', '')
    match_type = match_subtype_to_type[match_subtype_id]

    return render_template(
        'league-info.html', 
        schedule_for_eu = {
            'days': schedule_for_eu
        },
        schedule_for_us = {
            'days': schedule_for_us
        },
        year=date.today().year,
        title='Sumo Bar League',
        match_types=match_types,
        match_subtype=match_types[match_type][match_subtype_id]
    )

@app.route('/matches')
def matches():
    page = request.args.get('page', 1, type=int)
    match_subtype_id = request.args.get('match_subtype_id', '')
    match_type = match_subtype_to_type[match_subtype_id]
    
    matches = Match.query.filter(Match.matchtype == match_subtype_id).order_by(Match.date.desc(), Match.name.desc()).paginate(page, app.config['MATCHES_PER_PAGE'], False)
    next_url = url_for('matches', page=matches.next_num, match_subtype_id=match_subtype_id) \
        if matches.has_next else None
    prev_url = url_for('matches', page=matches.prev_num, match_subtype_id=match_subtype_id) \
        if matches.has_prev else None

    total_matches = matches.total

    return render_template(
        'matches.html',
        matches = matches.items,
        matchtype = match_subtype_id.replace("-", " ").upper(),
        match_types=match_types,
        year=date.today().year,
        match_subtype=match_types[match_type][match_subtype_id], 
        prev_url = prev_url, 
        next_url = next_url,
        total_matches = total_matches
    )

@app.route('/matches/update')
def updateMatches():
    client = secretmanager.SecretManagerServiceClient()
    key = request.args.get('key', '')
    actual_key= client.access_secret_version('projects/794715043730/secrets/MATCH_ADMIN_KEY/versions/latest').payload.data
    if (key == actual_key):
        execfile("scripts/import_data.py")
        os.system("python /home/ranking_app/scripts/import_GCP_storage_data.py")
        os.system("python /home/ranking_app/scripts/rank_trueskill.py")
        return "stuff"
    else:
        return "not stuff"