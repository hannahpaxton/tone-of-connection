"""Server for Tone of Connection app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, Post, Result
import crud
import asyncio

from jinja2 import StrictUndefined
from datetime import datetime
import os
import json
from colour import Color

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

GEOCODE_KEY = os.environ['GEOCODE_KEY']
from geocodio import GeocodioClient

client = GeocodioClient(GEOCODE_KEY)

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Hompage routes
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/login')
def login():
    """View login page."""

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register_user():
    """Create a new user"""

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else: 
        crud.create_user(username, password, email)
        flash('Account created!') 
    return redirect('/login')

@app.route('/create-session', methods=['POST'])
def login_user():
    """Login an existing user"""

    email = request.form.get('email_login')
    password = request.form.get('password_login')

    user = crud.get_user_by_password(email,password)
    if user:
        session['user_id'] = user.user_id
        flash('Logged in!')
    else: 
        flash('Password does not match. Try again.')
    return redirect(f"/users/{session['user_id']}")

@app.route('/logout')
def logout(): 
    if session.get('user_id'):
        del session['user_id']
    flash('You are now logged out.')
    return redirect('/')

# User routes
@app.route('/users')
def all_users():
    """View all users (TESTING ONLY)."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """User profile page"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

# Input routes
@app.route('/post')
def post_home():
    """View post home"""
    return render_template('post_homepage.html')

@app.route('/input', methods=['POST'])
def create_post():
    """Create a post and save in database"""

    # Get post text
    post_text = request.form.get('user_post')

    # Get user location 
    zipcode = request.form.get('zipcode')
    location_result = client.geocode(zipcode)
 
    lat = location_result["results"][0]["location"]["lat"]
    lng = location_result["results"][0]["location"]["lng"]	

    # Create post timestamp
    created_at = datetime.now()
    user_facing_date = created_at.strftime("%B %d, %Y")

    # Save post and related data to database
    post = crud.create_post(session['user_id'], post_text, lat, lng, created_at)

    return render_template('post_data.html', post=post, location_result=location_result, user_facing_date=user_facing_date)
    # return render_template('tone_result.html', final_results=final_results)

    # put in a different file - or the top of the file 
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
            tone_quality = crud.get_tone_by_tone_name(tone_name)

            score = tone_results["score"]
            score_conversion_delta = .5 - (score / 2)
            luminance_value = str(.5 + score_conversion_delta)
            c1 = Color(tone_quality.hex_base_value)
            c1.luminance = luminance_value
            unique_hex_value = c1.hex

            result = crud.create_result(post.post_id, tone_name, score, unique_hex_value)
            final_results.append(result)
 
@app.route('/api/tone/<int:post_id>')
def tone_info(post_id):
    """Return tone analysis from the database as JSON."""

    post = crud.get_post_by_post_id(post_id)
    analyze_post(post)

    tone_results = [
        {
            "tone_quality": tone_result.tone_quality,
            "tone_score": tone_result.tone_score,
            "hex_value": tone_result.hex_value,
        }
        for tone_result in Result.query.filter(Result.post_id==post_id).all()
    ]

    return jsonify(tone_results)

@app.route('/api/posts')
def post_info():
    """JSON information about all posts for map markers."""

    posts = [
        {
            "post_id": post.post_id,
            "user_id": post.user_id,
            "post_text": post.post_text,
            "lat": post.lat,
            "lng": post.lng,
            "created_at": post.created_at,
            "color": crud.get_color_by_post_id(post.post_id)
        }
        for post in Post.query.limit(50)
    ]

    return jsonify(posts)

@app.route('/tones')
def all_tone_qualities():
    """View all tones (TESTING ONLY)."""

    tone_qualities = crud.get_tone_qualities()

    return render_template('all_tone_qualities.html', tone_qualities=tone_qualities)

# Map routes

@app.route('/map')
def view_map():
    """View map."""

    return render_template('render_map.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)