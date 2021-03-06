"""Server for Tone of Connection app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, Post, Result
import crud
from sqlalchemy import desc
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

    if 'user_id' in session:
        return redirect(f"/users/{session['user_id']}")
    else:
        return render_template('home.html')

@app.route('/account')
def create_account():
    """View account creation page."""

    return render_template('account.html')

@app.route('/login')
def login():
    """View login page"""

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register_user():
    """Create a new user"""

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
        return redirect('/')
    else: 
        crud.create_user(username, email, password)
        flash('Account created!') 
        return redirect('/login')

@app.route('/create-session', methods=['POST'])
def login_user():
    """Login an existing user"""

    email = request.form.get('email_login')
    password = request.form.get('password_login')

    user = crud.get_user_by_password(email, password)
    if user:
        session['user_id'] = user.user_id
        flash('Logged in!')
        return redirect(f"/users/{session['user_id']}")
    else: 
        flash('Password does not match. Try again.')
        return redirect('/login')

@app.route('/logout')
def logout(): 
    """Logout an existing user"""

    if session.get('user_id'):
        del session['user_id']
    flash('You are now logged out.')
    return redirect('/login')

@app.route('/home')
def homepage_log():
    """View homepage when a user is logged in."""

    return render_template('home_log.html')

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

    random_prompt = crud.get_random_prompt()

    return render_template('post_homepage.html', random_prompt=random_prompt)

@app.route('/geocode')
def geocode_zip():
    """Geocode a user's zipcode"""

    # Get user location 
    zipcode = request.args.get('zipcode')
    location_result = client.geocode(zipcode)

    # Save needed geolocation in the session
    session['lat'] = location_result["results"][0]["location"]["lat"]
    session['lng']= location_result["results"][0]["location"]["lng"]

    city = location_result["results"][0]["address_components"]["city"]
    state = location_result["results"][0]["address_components"]["state"]
    session['user_facing_location'] = city + ", " + state

    return jsonify(location_result)

@app.route('/input', methods=['POST'])
def create_post():
    """Create a post and save in database"""

    #Get prompt id
    prompt_id = request.form.get('prompt_id')

    # Get post text
    post_text = request.form.get('user_post')

    # Create post timestamp
    created_at = datetime.now()
    user_facing_date = created_at.strftime("%B %d, %Y")

    # Save post and related data to database
    post = crud.create_post(session['user_id'], prompt_id, post_text, session['lat'], session['lng'], session['user_facing_location'], created_at)

    return render_template('post_data.html', post=post, user_facing_date=user_facing_date)
  
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
            "prompt": crud.get_prompt_by_prompt_id(post.prompt_id),
            "post_text": post.post_text,
            "lat": post.lat,
            "lng": post.lng,
            "created_at": post.created_at,
            "color": crud.get_max_color_by_post_id(post.post_id),
        }
        for post in Post.query.order_by(desc(Post.created_at)).limit(200)
    ]

    return jsonify(posts)

@app.route('/tones')
def all_tone_qualities():
    """View all tones (TESTING ONLY)."""

    tone_qualities = crud.get_tone_qualities()

    return render_template('all_tone_qualities.html', tone_qualities=tone_qualities)

@app.route('/posts_filtered')
def view_filtered_post():
    """View filtered posts."""

    user = crud.get_user_by_id(session['user_id'])
    tone_quality = request.args.get('tone_filter_quality')

    return render_template('user_details_filtered.html', user=user, tone_quality=tone_quality)

# React routes

@app.route("/posts.json")
def get_all_posts_json():
    """Return a JSON response with all of a user's posts."""

    posts = [
        {
            "postId": post.post_id,
            "postPrompt" : crud.get_prompt_by_prompt_id(post.prompt_id),
            "postText": post.post_text,
            "location": post.user_facing_location,
            "dateCreated": post.created_at,
            "toneQualities": crud.get_tone_qualities_by_post_id(post.post_id),
        }
        for post in crud.get_post_by_user_id(session['user_id'])
    ]

    return jsonify(posts)

@app.route("/posts_filtered/<tone_filter>")
def get_filtered_posts_json(tone_filter):
    """Return a JSON response with a filtered selection of a user's posts."""

    posts = [
        {
            "postId": post.post_id,
            "postPrompt" : crud.get_prompt_by_prompt_id(post.prompt_id),
            "postText": post.post_text,
            "location": post.user_facing_location,
            "dateCreated": post.created_at,
            "toneQualities": crud.get_tone_qualities_by_post_id(post.post_id),
        }
        for post in crud.get_post_by_tone_quality(session['user_id'], tone_filter)
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