"""Server for Tone of Connection app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Hompage routes
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

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
    return redirect('/')

@app.route('/login', methods=['POST'])
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

# Tone routes
@app.route('/tones')
def all_tone_qualities():
    """View all tones (TESTING ONLY)."""

    tone_qualities = crud.get_tone_qualities()

    return render_template('all_tone_qualities.html', tone_qualities=tone_qualities)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)