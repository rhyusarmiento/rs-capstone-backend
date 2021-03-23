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

player_teams = db.Table('player_teams',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    state = db.Column(db.String(2), unique=False, nullable=False)
    phone_number = db.Column(db.String(13), unique=False, nullable=False)
    teams = db.relationship(
        'Team',
        secondary=player_teams, 
        lazy='subquery', 
        backref=db.backref('player', lazy=True),
    )

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    city = db.Column(db.String(20), unique=False)
    state = db.Column(db.String(2), unique=False)
    sport = db.Column(db.String(15), unique=False)
    matchup = db.relationship('Matchup', backref='team', lazy=True)

class Matchup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    when = db.Column(db.String(30), unique=False)
    where = db.Column(db.String(20), unique=False)
    team1 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    active = db.Column(db.Boolean, unique=False)

class PlayerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'city', 'state', 'phone_number', 'teams')

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

class TeamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'city', 'state', 'sport', 'matchup')

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

class MatchupSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'city', 'state', 'sport', 'matchup')

matchup_schema = MatchupSchema()
matchups_schema = MatchupSchema(many=True)

@app.route('/api/add-player', methods=['POST'])
def add_player():
    post_data = request.get_json()
    name = post_data.get('name')
    city = post_data.get('city')
    state = post_data.get('state')
    phone_number = post_data.get('phone_number')
    # teams = post_data.get('teams')
    new_player = Player(name=name, city=city, state=state, phone_number=phone_number)
    db.session.add(new_player)
    db.session.commit()
    return jsonify(player_schema.dump(new_player))

@app.route('/api/get-players')
def get_players():
    all_players = Player.query.all()
    return jsonify(players_schema.dump(all_players))

# @app.route('/api/add-player', methods=['POST'])
# def add_player():
#     post_data = request.get_json()
#     name = post_data.get('name')
#     city = post_data.get('city')
#     state = post_data.get('state')
#     phone_number = post_data.get('phone_number')
#     # teams = post_data.get('teams')
#     new_player = Player(name=name, city=city, state=state, phone_number=phone_number)
#     db.session.add(new_player)
#     db.session.commit()
#     return jsonify(player_schema.dump(new_player))

if __name__ == '__main__':
    app.run(debug=True)