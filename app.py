from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    city = db.Column(db.String(20), unique=False)
    state = db.Column(db.String(2), unique=False)
    phone_number = db.Column(db.String(13), unique=False)
    teams = db.relationship('player_teams', backref=db.backref('player', lazy=True))
    
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    city = db.Column(db.String(20), unique=False)
    state = db.Column(db.String(2), unique=False)
    sport = db.Column(db.String(15), unique=False)
    players = db.relationship('player_teams', backref=db.backref('team', lazy=True))
    matchup = db.relationship('Matchup', backref=db.backref('team', lazy=True))

class player_teams(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

class Matchup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    when = db.Column(db.String(30), unique=False)
    where = db.Column(db.String(20), unique=False)
    team1 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    active = db.Column(db.String(15), unique=False)