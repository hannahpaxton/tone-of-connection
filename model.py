"""Models for Tone of Connection app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///tones', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    posts = db.relationship('Post', backref='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'

class Post(db.Model):
    """A post."""

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    user_id = db.Column(db.Integer,
    db.ForeignKey('users.user_id'))
    prompt_id = db.Column(db.Integer,
    db.ForeignKey('prompts.prompt_id'))
    post_text = db.Column(db.String)
    lat = db.Column(db.Float(10))
    lng = db.Column(db.Float(10))
    user_facing_location = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    tone_results = db.relationship('Result', backref='post')
    prompt = db.relationship('Prompt', backref='post')
    # user (comes from backref in posts)

    def __repr__(self):
        return f'<Post post_id={self.post_id} created_at={self.created_at}>'

class Result(db.Model):
    """A tone result from a user text input."""

    __tablename__ = 'tone_results'

    tone_id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    post_id = db.Column(db.Integer,
    db.ForeignKey('posts.post_id'))
    tone_quality = db.Column(db.String,
    db.ForeignKey('tone_qualities.tone_quality'))
    tone_score = db.Column(db.Float)
    hex_value = db.Column(db.String)

    tone_qualities = db.relationship('Quality', backref='tone_results')
    # post (comes from backref in tone_results)

    def __repr__(self):
        return f'<Result tone_quality={self.tone_quality} tone_score={self.tone_score}>'

class Quality(db.Model):
    """All possible tone qualities that can be produced."""

    __tablename__ = 'tone_qualities'
    tone_quality = db.Column(db.String,
                unique=True,
                primary_key=True)
    hex_base_value = db.Column(db.String)

    # tone_results (comes from backref in tone_qualities)

    def __repr__(self):
        return f'<Quality tone_quality={self.tone_quality} hex_base_value={self.hex_base_value}>'

class Prompt(db.Model):
    """All possible post prompts."""

    __tablename__ = 'prompts'
    prompt_id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    prompt = db.Column(db.String)

    # post (comes from backref in prompts)

    def __repr__(self):
        return f'<Prompt prompt_id={self.prompt_id}>'

if __name__ == '__main__':
    # from server import app

    connect_to_db(app)