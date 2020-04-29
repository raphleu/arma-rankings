from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    matchtype = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    results = db.Column(db.String(1000))

    def __repr__(self):
        return '<Match {}>'.format(self.name)

class Elorating(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), db.ForeignKey('user.username'))
    matchtype = db.Column(db.String(64))
    rating = db.Column(db.Integer)

    def __repr__(self):
        return '<EloRating {}>'.format(self.user_id)
