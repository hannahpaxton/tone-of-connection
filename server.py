"""Server for Tone of Connection app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, Post
import crud

from jinja2 import StrictUndefined
from datetime import datetime
import os
import json

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

    post_text = request.form.get('user_post')

    zipcode = request.form.get('zipcode')
    location_result = client.geocode(zipcode)
    print(location_result)

    lat = location_result["results"][0]["location"]["lat"]
    lng = location_result["results"][0]["location"]["lng"]	

    created_at = datetime.now()

    post = crud.create_post(session['user_id'], post_text, lat, lng, created_at)

    tone_analysis = tone_analyzer.tone(
        {'post_text': post_text},
        content_type='text/plain',
        sentences='false'
         ).get_result()
    print(json.dumps(tone_analysis))

    final_results = []

    for tone_results in tone_analysis["document_tone"]["tones"]:
            tone_name = tone_results["tone_name"]
            tone_quality = crud.get_tone_by_tone_name(tone_name)

            score = tone_results["score"]
            score_conversion_delta = 50 - int(round(score * 100 / 2))
            lightness_value = str(50 + score_conversion_delta)
            unique_hsl_value = tone_quality.hsl_base_value + lightness_value + "%)"

            result = crud.create_result(post.post_id, tone_name, score, unique_hsl_value)
            final_results.append(result)

    return render_template('tone_result.html', final_results=final_results)
# Post routes

@app.route('/api/posts')
def post_info():
    """JSON information about posts."""

    posts = [
        {
            "post_id": post.post_id,
            "user_id": post.user_id,
            "post_text": post.post_text,
            "lat": post.lat,
            "lng": post.lng,
            "created_at": post.created_at,
        }
        for post in Post.query.limit(50)
    ]

    return jsonify(posts)

# Tone routes

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