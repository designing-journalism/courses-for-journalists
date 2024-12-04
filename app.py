from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from src.models import db, Course, User
from typing import List

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Change this to your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Define your routes
@app.route('/')
def home():
    error_message = None
    try:
        # You can add any logic here that might raise an exception
        return render_template('index.html', error_message=error_message)
    except Exception as e:
        error_message = str(e)  # Capture the error message
        return render_template('index.html', error_message=error_message)

@app.route('/courses')
def courses_page():
    courses = Course.query.filter_by(status='active').all()  # Fetch only active courses
    quiz_questions = [
        {
            "question_nr": 1,  # Question number
            "question": "Welke stelling past het beste bij jou?",
            "answers": [
                {"text": "Je weet wat AI is, maar gebruikt het niet of nauwelijks bewust", "score": 1},
                {"text": "Je gebruikt AI oppervlakkig en soms in je werk, voornamelijk generatieve AI ter ondersteuning van je werkzaamheden", "score": 2},
                {"text": "Je gebruikt AI regelmatig in projecten en je werkzaamheden en hebt mogelijk al geëxperimenteerd met het bouwen van modellen met een ICT-er", "score": 3},
                {"text": "Je hebt veel kennis en kan zelf AI Modellen bouwen", "score": 4}
            ]
        },
        {
            "question_nr": 2,  # Question number
            "question": "Hoe vaak gebruik je in jouw werkzaamheden technologieën als kunstmatige intelligentie?",
            "answers": [
                {"text": "Zelden tot nooit", "score": 1},
                {"text": "Af en toe", "score": 3},
                {"text": "Periodiek", "score": 6},
                {"text": "Dagelijks", "score": 10}
            ]
        },
        {
            "question_nr": 3,  # Question number
            "question": "Hoe schat je jouw eigen kennis en vaardigheid in rond inzet van kunstmatige intelligentie?",
            "answers": [
                {"text": "Ik ben er niet of nauwelijks mee bekend", "score": 1},
                {"text": "Ik ben bekend met de belangrijke concepten en termen van kunstmatige intelligentie", "score": 3},
                {"text": "Ik weet wat generatieve AI is en welke generatieve AI-systemen in zou kunnen gebruiken in mijn werk", "score": 5},
                {"text": "Ik heb generatieve AI-tekstsystemen, beeldgeneratiesystemen of andere generatieve AI-systemen ingezet", "score": 7},
                {"text": "Ik heb enige ervaring met het gebruiken van AI in projecten", "score": 10},
                {"text": "Ik heb ervaring met het bouwen van AI-modellen (alleen of samen met een ICT’er)", "score": 20}
            ]
        },
        {
            "question_nr": 4,  # Question number
            "question": "Kies het onderwerp dat je het meest interesseert:",
            "answers": [
                {"text": "Machinelearning en AI", "topic": "MLAI"},
                {"text": "Data analysis and cleaning", "topic": "DACL"},
                {"text": "AI, ethiek en maatschappelijke gevolgen", "topic": "AIETHIC"},
                {"text": "Generatieve AI & Prompting", "topic": "GENAI"},
            ]
        },
    ]
    return render_template('courses.html', courses=courses, quiz_questions=quiz_questions)

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
        status = request.form.get('status')  # 'active' or 'archived'

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
                db.session.commit()
        else:
            # Add new course
            new_course = Course(title=title, description=description, duration=duration, level=level, status=status)
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

        # Check if we are editing an existing user
        user_id = request.form.get('user_id')
        if user_id:
            # Update existing user
            user = User.query.get(user_id)
            if user:
                user.username = username
                user.email = email
                db.session.commit()
        else:
            # Add new user
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()

        return redirect('/manage_users')  # Redirect to the same page after submission

    # Fetch all users for display
    users = User.query.all()
    return render_template('manage_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for easier troubleshooting
