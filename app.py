from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from src.models import db, Course, User
from typing import List
from src.utils import calculate_relevancy_points, get_logged_in_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure this is set for session management

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Change this to your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Define your routes
@app.route('/')
def index():
    error_message = None
    try:
        # You can add any logic here that might raise an exception
        return render_template('index.html', error_message=error_message)
    except Exception as e:
        error_message = str(e)  # Capture the error message
        return render_template('index.html', error_message=error_message)

@app.route('/courses', methods=['GET', 'POST'])
def courses_page():
    search_text = request.form.get('search_text', '')
    level = request.form.get('level', '')
    quiz_answers = request.form.getlist('quiz_answers')  # Assuming quiz answers are sent as a list

    user = get_logged_in_user()  # Get the current logged-in user
    courses = Course.query.filter_by(status='active').all()

    # Calculate relevancy points
    sorted_courses = calculate_relevancy_points(user, courses, search_text, level, quiz_answers)

    return render_template('courses.html', courses=sorted_courses)

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/api/courses')
def get_courses():
    try:
        courses = Course.query.filter_by(status='active').all()  # Fetch only active courses
        # Convert each course instance to a dictionary
        return jsonify([{
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'duration': course.duration,
            'level': course.level,
            'status': course.status
        } for course in courses])  # Adjust as necessary
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/manage_courses', methods=['GET', 'POST'])
def manage_courses():
    if request.method == 'POST':
        # Handle form submission for adding or editing courses
        title = request.form.get('title')
        description = request.form.get('description')
        duration = request.form.get('duration')
        level = request.form.get('level')
        status = request.form.get('status')
        tags = request.form.get('tags')  # New field for tags

        # Check if we are editing an existing course
        course_id = request.form.get('course_id')
        if course_id:
            # Update existing course
            course = Course.query.get(course_id)
            if course:
                course.title = title
                course.description = description
                course.duration = duration
                course.level = level
                course.status = status
                course.tags = tags  # Update tags
                db.session.commit()
        else:
            # Add new course
            new_course = Course(title=title, description=description, duration=duration, level=level, status=status, tags=tags)
            db.session.add(new_course)
            db.session.commit()

        return redirect('/manage_courses')  # Redirect to the same page after submission

    # Fetch all courses for display
    courses = Course.query.all()
    return render_template('manage_courses.html', courses=courses)

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        # Handle form submission for adding or editing users
        username = request.form.get('username')
        email = request.form.get('email')
        tags = request.form.get('tags')  # New field for tags

        # Check if we are editing an existing user
        user_id = request.form.get('user_id')
        if user_id:
            # Update existing user
            user = User.query.get(user_id)
            if user:
                user.username = username
                user.email = email
                user.tags = tags  # Update tags
                db.session.commit()
        else:
            # Add new user without a password
            new_user = User(username=username, email=email, tags=tags)
            db.session.add(new_user)
            db.session.commit()

        return redirect('/manage_users')  # Redirect to the same page after submission

    # Fetch all users for display
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Still capture the password input
        # Bypass password verification
        user = User.query.filter_by(username=username).first()
        if user:  # Assume login is successful if the user exists
            session['username'] = username  # Store the username in the session
            return redirect(url_for('index'))  # Redirect to the homepage or another page
        else:
            # Handle login failure (e.g., show an error message)
            return render_template('login.html', error="User not found")
    return render_template('login.html')  # Render the login template

@app.route('/logout')
def logout():
    session.pop('username', None)  # Verwijder de gebruikersnaam uit de sessie
    return redirect(url_for('index'))  # Redirect naar de hoofdpagina

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for easier troubleshooting
