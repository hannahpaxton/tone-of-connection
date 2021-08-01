"""CRUD operations."""

from model import db, User, Post, Result, Quality, Prompt, connect_to_db
from datetime import datetime
from sqlalchemy import func, select, desc
import os
import json
from colour import Color

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

def get_post_by_tone_quality(user_id, tone_quality):
    """Get posts by tone quality and user_id"""

    needed_post_ids = db.session.query(Result.post_id).filter(Result.tone_quality == tone_quality).all()
    needed_posts = db.session.query(Post).filter(Post.post_id.in_(needed_post_ids), Post.user_id == user_id).order_by(desc(Post.created_at)).all()
    
    return needed_posts
    
def create_post(user_id, prompt_id, post_text, lat, lng, user_facing_location, created_at):
    """Create and return a user post"""

    post = Post(user_id=user_id, prompt_id=prompt_id, post_text=post_text, lat=lat, lng=lng, user_facing_location=user_facing_location, created_at=created_at)

    db.session.add(post)
    db.session.commit()

    return post

def create_result(post_id, tone_quality, tone_score, hex_value):
    
    result = Result(post_id=post_id, tone_quality=tone_quality, tone_score=tone_score, hex_value=hex_value)

    db.session.add(result)
    db.session.commit()

    return result

def create_prompt(prompt):
    """Create and return all post prompts"""

    prompt = Prompt(prompt=prompt)

    db.session.add(prompt)
    db.session.commit()

    return prompt

def get_random_prompt():
    """Get random prompt from the database"""

    return db.session.query(Prompt).order_by(func.random()).limit(1).one()

def get_prompt_by_prompt_id(prompt_id):
    """View prompt by prompt_id"""
 
    used_prompt = db.session.query(Prompt.prompt).filter(Prompt.prompt_id == prompt_id).one()
    return used_prompt[0]

def create_tone_quality(tone_quality, hex_base_value):
    """Create and return all tone quality possibilities"""

    tone_quality = Quality(tone_quality=tone_quality, hex_base_value=hex_base_value)

    db.session.add(tone_quality)
    db.session.commit()

    return tone_quality

def get_tone_qualities():
    """View all tone_qualities"""

    return Quality.query.all()

def get_tone_by_tone_name(tone_name):
    """View tone by tone_name"""

    return Quality.query.filter(Quality.tone_quality == tone_name).first()

def get_post_by_post_id(post_id):
    """View post by post_id"""

    return Post.query.filter(Post.post_id == post_id).first()

def get_tone_qualities_by_post_id(post_id):
    """View tone qualities by post_id"""

    return db.session.query(Result.tone_quality, Result.hex_value, Result.tone_id, Result.tone_score).filter(Result.post_id == post_id).all()

def get_post_by_user_id(user_id):
    """View post by user_id"""

    return Post.query.filter(Post.user_id == user_id).order_by(desc(Post.created_at)).all()

def get_prompt_by_prompt_id(prompt_id):
    """View prompt by prompt_id"""

    return db.session.query(Prompt.prompt).filter(Prompt.prompt_id == prompt_id).one()


def get_max_color_by_post_id(post_id):
    """Return the color of the max tone score for a given post"""

    ordered_records = db.session.query(Result).filter(Result.post_id == post_id).order_by(Result.tone_score.desc()).all()
    if ordered_records:
        return ordered_records[0].hex_value
    else:
        return "#FFFFFF"

# Tone Analyzer API 
API_KEY = os.environ['TONE_KEY']
ENDPOINT = os.environ['URL']
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(API_KEY)
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)
tone_analyzer.set_service_url(ENDPOINT)

def analyze_post(post):

    tone_analysis = tone_analyzer.tone(
        {'post_text': post.post_text},
        content_type='text/plain',
        sentences='false'
         ).get_result()
    print(json.dumps(tone_analysis))

    final_results = []

    for tone_results in tone_analysis["document_tone"]["tones"]:
            tone_name = tone_results["tone_name"]
            tone_quality = get_tone_by_tone_name(tone_name)

            score = tone_results["score"]
            score_conversion_delta = .8 - (score / 1.2)
            luminance_value = str(.5 + score_conversion_delta)
            c1 = Color(tone_quality.hex_base_value)
            c1.luminance = luminance_value
            unique_hex_value = c1.hex

            score_percentage = (100 * score)
            user_facing_score = "{:.2f}".format(score_percentage)

            result = create_result(post.post_id, tone_name, user_facing_score, unique_hex_value)
            final_results.append(result)

    return final_results
       
    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)