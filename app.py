import os
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'secret'
app.secret_key = os.environ.get('SECRET_KEY')
app.permanent_session_lifetime = timedelta(minutes=1)
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
ma = Marshmallow(app)
flask_bcrypt = Bcrypt(app)

players_teams = db.Table('players_teams',
    db.Column(
        'player_id', 
        db.Integer, 
        db.ForeignKey('player.id', ondelete="CASCADE"),
    ),
    db.Column(
        'team_id', 
        db.Integer, 
        db.ForeignKey('team.id', ondelete="CASCADE"),
    )
)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(30), unique=False, nullable=False)
    state = db.Column(db.String(2), unique=False, nullable=False)
    phone_number = db.Column(db.String(13), unique=False, nullable=False)
    teams = db.relationship(
        'Team',
        secondary=players_teams, 
        lazy='subquery', 
        back_populates='players',
        # cascade="all, delete",
    )

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    state = db.Column(db.String(2), unique=False, nullable=False)
    sport = db.Column(db.String(15), unique=False, nullable=False)
    players = db.relationship(
        'Player',
        secondary=players_teams, 
        lazy='subquery', 
        back_populates='teams',
        # passive_deletes=True
    )

# class Matchup(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     when = db.Column(db.String(30), unique=False, nullable=False)
#     where = db.Column(db.String(20), unique=False, nullable=False)
#     team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
#     team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
#     active = db.Column(db.Boolean, unique=False, nullable=False)
#     team1 = db.relationship('Matchup', foreign_keys=[team1_id])
#     team2 = db.relationship('Matchup', foreign_keys=[team2_id])

class PlayerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'name', 'city', 'state', 'phone_number')

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

class TeamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'city', 'state', 'sport')

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

# class MatchupSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'when', 'where', 'team1_id', 'team2_id', 'active')

# matchup_schema = MatchupSchema()
# matchups_schema = MatchupSchema(many=True)

@app.route('/api/register', methods=['POST'])
def register():
    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')
    name = post_data.get('name')
    city = post_data.get('city')
    state = post_data.get('state')
    phone_number = post_data.get('phone_number')
    db_player = Player.query.filter_by(username=username).first()
    if db_player:
        return 'username taken', 404
    hashed_password = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    new_player = Player(username=username, password=hashed_password, name=name, city=city, state=state, phone_number=phone_number)
    db.session.add(new_player)
    db.session.commit()
    session.permanent = True
    session['username'] = username
    print(session)
    return jsonify(player_schema.dump(new_player))

@app.route('/api/login', methods=['POST'])
def login():
    post_data = request.get_json()
    db_player = Player.query.filter_by(username=post_data.get('username')).first()
    if db_player is None:
        return 'username not found', 404
    password = post_data.get('password')
    db_player_hashed_password = db_player.password
    valid_password = flask_bcrypt.check_password_hash(db_player_hashed_password, password)
    if valid_password:
        session.permanent = True
        session['username'] = post_data.get('username')
        return jsonify('user verified')
    return 'password invalid', 401

@app.route('/api/logged-in', methods=['GET'])
def logged_in():
    if 'username' in session:
        db_player = Player.query.filter_by(username=session['username']).first()
        if db_player:
            return jsonify('User Logged Via Cookie')
        else:
            return jsonify('session exists, but user does not exist ... anymore')
    else:
        return jsonify('nope!')

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify('Logged out')

# Player CRUD
# add_player was here merged with register

@app.route('/api/get-players')
def get_players():
    all_players = Player.query.all()
    return jsonify(players_schema.dump(all_players))

@app.route('/api/get-single-player/<id>')
def get_single_player(id):
    player = Player.query.get(id)
    return jsonify(player_schema.dump(player))

@app.route('/api/edit-player/<id>', methods=['POST'])
def edit_player(id):
    player = Player.query.get(id)
    post_data = request.get_json()
    player.name = post_data.get('name')
    player.city = post_data.get('city')
    player.state = post_data.get('state')
    player.phone_number = post_data.get('phone_number')
    db.session.commit()
    return jsonify(player_schema.dump(player))

@app.route('/api/delete-player/<id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get(id)
    db.session.delete(player)
    db.session.commit()
    return jsonify('done')

# Team CRUD
@app.route('/api/add-team', methods=['POST'])
def add_team():
    post_data = request.get_json()
    name = post_data.get('name')
    city = post_data.get('city')
    state = post_data.get('state')
    sport = post_data.get('sport')
    new_team = Team(name=name, city=city, state=state, sport=sport)
    db.session.add(new_team)
    db.session.commit()
    return jsonify(player_schema.dump(new_team))

@app.route('/api/get-teams')
def get_teams():
    all_teams = Team.query.all()
    return jsonify(teams_schema.dump(all_teams))

@app.route('/api/get-single-team/<id>')
def get_single_team(id):
    team = Team.query.get(id)
    return jsonify(team_schema.dump(team))

@app.route('/api/edit-team/<id>', methods=['POST'])
def edit_team(id):
    team = Team.query.get(id)
    post_data = request.get_json()
    team.name = post_data.get('name')
    team.city = post_data.get('city')
    team.state = post_data.get('state')
    team.sport = post_data.get('sport')
    db.session.commit()
    return jsonify(team_schema.dump(team))

@app.route('/api/delete-team/<id>', methods=['DELETE'])
def delete_team(id):
    team = Team.query.get(id)
    db.session.delete(team)
    db.session.commit()
    return jsonify('done')

# many 2 many
@app.route('/api/player-join-team/<player_id>/<team_id>')
def join_team(player_id, team_id):
    player = Player.query.get(player_id)
    team = Team.query.get(team_id)
    player.teams.append(team)
    db.session.commit()
    return jsonify(teams_schema.dump(player.teams))

@app.route('/api/get-players-team/<id>')
def get_players_team(id):
    team = Team.query.get(id)
    return jsonify(players_schema.dump(team.players))

@app.route('/api/get-teams-player/<id>')
def get_teams_player(id):
    player = Player.query.get(id)
    return jsonify(teams_schema.dump(player.teams))

if __name__ == '__main__':
    app.run(debug=True)