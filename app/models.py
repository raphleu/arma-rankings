from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    matchtype = db.Column(db.String(64))
    date = db.Column(db.Date)
    quality = db.Column(db.Float())

    def __repr__(self):
        return '<Match {}>'.format(self.id)

class Elorating(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), db.ForeignKey('user.username'))
    matchtype = db.Column(db.String(64))
    rating = db.Column(db.Integer)
    latest_delta = db.Column(db.Integer)

    def __repr__(self):
        return '<EloRating {}>'.format(self.username)

class Trueskillrating(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), db.ForeignKey('user.username'))
    matchtype = db.Column(db.String(64))
    mu = db.Column(db.Float())
    sigma = db.Column(db.Float())
    rating = db.Column(db.Integer)
    latest_delta = db.Column(db.Integer)
    latest_delta_date = db.Column(db.Date)

    def __repr__(self):
        return '<TrueskillRating {}>'.format(self.username)

class MatchScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    username = db.Column(db.String(64), db.ForeignKey('user.username'))
    score = db.Column(db.Integer)
    place = db.Column(db.Integer)
    match = relationship("Match", back_populates="match_scores")

    def __repr__(self):
        return '<MatchScore {}>'.format(self.username)

Match.match_scores = relationship("MatchScore", order_by = MatchScore.place, back_populates = "match")
