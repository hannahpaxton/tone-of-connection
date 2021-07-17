"""Server for Tone of Connection app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, Post, Result
import crud

from jinja2 import StrictUndefined
from datetime import datetime
import os
import json

# Geocoding API
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

    # Add city and state to database
    # city = location_result["results"][0]["address_components"]["city"]
    # state = location_result["results"][0]["address_components"]["state"]
    # user_facing_location = city + state

    # Create post timestamp
    created_at = datetime.now()
    user_facing_date = created_at.strftime("%B %d, %Y")

    # Save user facing location to database 
    # Save post and related data to database
    post = crud.create_post(session['user_id'], post_text, lat, lng, created_at)

    return render_template('post_data.html', post=post, location_result=location_result, user_facing_date=user_facing_date)
  
@app.route('/api/tone/<int:post_id>')
def tone_info(post_id):
    """Return tone analysis from the database as JSON."""

    post = crud.get_post_by_post_id(post_id)
    crud.analyze_post(post)

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
            "color": crud.get_max_color_by_post_id(post.post_id),
        }
        for post in Post.query.limit(200)
    ]

    return jsonify(posts)

@app.route('/tones')
def all_tone_qualities():
    """View all tones (TESTING ONLY)."""

    tone_qualities = crud.get_tone_qualities()

    return render_template('all_tone_qualities.html', tone_qualities=tone_qualities)

# React routes

@app.route("/posts.json")
def get_posts_json():
    """Return a JSON response with all of a user's posts."""


    posts = [
        {
            "postId": post.post_id,
            "postText": post.post_text,
            "lat": post.lat,
            "dateCreated": post.created_at,
            "toneQualities": crud.get_tone_qualities_by_post_id(post.post_id),
        }
        for post in crud.get_post_by_user_id(session['user_id'])
    ]

    return jsonify(posts)

# Map routes

@app.route('/map')
def view_map():
    """View map."""

    return render_template('render_map.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)