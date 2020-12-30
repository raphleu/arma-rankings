from app import app, db, service
from app.app_config import schedule_for_us, schedule_for_eu, match_types, match_subtype_to_type
from app.models import Elorating, Trueskillrating, Match, MatchScore
from datetime import date, datetime, timedelta
from flask import render_template, request, url_for
from google.cloud import secretmanager
import json
import os
import random
from sqlalchemy import func
from sqlalchemy.dialects.mssql import INTEGER
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import coalesce

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

@app.route('/api/generate-teams', methods=['POST'])
def generateTeams():
    data = request.get_json() or {}
    players = data['players']
    response = service.generateTeamsService(players)
    return json.dumps(response)

@app.route('/api/players/exists', methods=['GET'])
def playerExists():
    username = request.args.get('username', '').lower()
    match_subtype_id = request.args.get('match_subtype_id', '')
    player_query = Trueskillrating.query.filter(func.lower(Trueskillrating.username) == username).filter(Trueskillrating.matchtype == match_subtype_id)
    player_count = player_query.count()
    return str(player_count)