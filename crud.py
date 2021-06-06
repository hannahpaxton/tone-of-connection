"""CRUD operations."""

from model import db, User, Post, Result, Quality, connect_to_db
from datetime import datetime

def create_user(username, password, email):
    """Create and return a new user."""

    user = User(username=username, password=password, email=email)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    "View all users"

    return User.query.all()

def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    """Return a user by id"""

    return User.query.get(user_id)

def get_user_by_password(email,password):
    """Return a user by password."""

    return User.query.filter(User.password == password, User.email == email).first()

def create_tone_quality(tone_quality):
    """Create and return all tone quality possibilities"""

    tone_quality = Quality(tone_quality=tone_quality)

    db.session.add(tone_quality)
    db.session.commit()

    return tone_quality

def get_tone_qualities():
    "View all tone_qualities"

    return Quality.query.all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)