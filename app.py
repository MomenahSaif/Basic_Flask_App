from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect  # Import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_wtf import FlaskForm
from forms import SignupForm, LoginForm
import logging

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Your existing secret key

# Set up logging to log errors to a file
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Session management settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensures cookies are only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevents JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Helps mitigate CSRF attacks from other domains
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session lifetime (optional, 1 hour in seconds)

# Make the session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True  # Make session permanent

# Custom error handler for 404 errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Custom error handler for 500 errors
@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500

@app.route('/error')
def error():
    raise Exception('This is a test error for testing 500 page.')

def get_user_by_username(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

# Database connection and initialization
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  phone TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        phone = form.phone.data
        hashed_password = generate_password_hash(password)

        # Store in database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)',
                      (username, hashed_password, email, phone))
            conn.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'error')
        finally:
            conn.close()
    else:
        # Handle individual form validation errors
        flash('Signup unsuccessful.', 'error')

    return render_template('signup.html', form=form)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Form validation passed
        username = form.username.data
        password = form.password.data

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    else:
        # Debug: print form errors to the console
        print("Login form validation failed", form.errors)

    return render_template('login.html', form=form)

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
