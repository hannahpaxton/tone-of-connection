"""Models for Tone of Connection app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

class Post(db.Model):
    """A post."""

    __tablename__ = 'posts'

class Result(db.Model):
    """A tone result from a user text input."""

    __tablename__ = 'tone_results'

class Quality(db.Model):
    """All possible tone qualities that can be produced."""

    __tablename__ = 'tone_qualities'