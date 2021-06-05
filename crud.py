"""CRUD operations."""

from model import db, User, Post, Result, Quality, connect_to_db
from datetime import datetime

def create_user(username, password, email):
    """Create and return a new user."""

    user = User(user=user, password=password, email=email)

    db.session.add(user)
    db.session.commit()

    return user

def create_post(post_text, lat_long, datetime_saved):
    """Create and return a new post."""

    post = Post(post_text=post_text, lat_long=lat_long, datetime_saved=datetime_saved)

    db.session.add(post)
    db.session.commit()

    return user


if __name__ == '__main__':
    from server import app
    connect_to_db(app)