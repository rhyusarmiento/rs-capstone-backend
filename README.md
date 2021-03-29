# Backend

## Dependency Docs
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [Marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
- [flask-cors](https://flask-cors.readthedocs.io/en/latest/)

## Installing the server
- While in the `app` folder, run the following commands in your terminal 
```
$ pipenv install
```
- Or 
```
$ pipenv --three
```

## Starting the server
- While in the `app` folder, run the following commands in your terminal 
```
$ pipenv shell
(app) python app.py
```

## Create DataBase
- If you need to setup your database you will need to do the following inside a python repl while in your pipenv shell.
- Make sure to be within the `app` folder directory
```
>>> from app import db
>>> db.create_all()
```
- This will then add an app.sqlite file to your local computer

# api routes

> http://localhost:5000/api/register
> http://localhost:5000/api/login
> http://localhost:5000/api/logged-in
> http://localhost:5000/api/logout

- player 
> http://localhost:5000/api/get-players
> http://localhost:5000/api/get-single-player/<id>
> http://localhost:5000/api/edit-player/<id>
> http://localhost:5000/api/delete-player/<id>

- team
> http://localhost:5000/api/add-team
> http://localhost:5000/api/get-teams
> http://localhost:5000/api/get-single-team/<id>
> http://localhost:5000/api/edit-team/<id>
> http://localhost:5000/api/delete-team/<id>

- Many 2 Many
> http://localhost:5000/api/player-join-team/<player_id>/<team_id>
> http://localhost:5000/api/get-players-team/<id>
> http://localhost:5000/api/get-teams-player/<id>