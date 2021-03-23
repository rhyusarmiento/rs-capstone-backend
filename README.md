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