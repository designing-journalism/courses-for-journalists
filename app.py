from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from src.models import db, Course, User, Tag
from typing import List
from src.utils import calculate_relevancy_points, get_logged_in_user
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Ensure this is set for session management

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///your_database.db"  # Change this to your database URI
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)


# Define your routes
@app.route("/")
def index():
    error_message = None
    try:
        # You can add any logic here that might raise an exception
        return render_template("index.html", error_message=error_message)
    except Exception as e:
        error_message = str(e)  # Capture the error message
        return render_template("index.html", error_message=error_message)


@app.route("/courses", methods=["GET", "POST"])
def courses_page():
    # Fetch active courses
    courses = Course.query.filter_by(status="active").all()

    # Get the current logged-in user
    user = get_logged_in_user()

    # Split user tags by space
    user_tags = set(user.tags.split()) if user and user.tags else set()

    # Query all tags from the database
    all_tags = Tag.query.all()

    # Prepare quiz questions (as before)
    quiz_questions = [
        {
            "question_nr": 1,  # Question number
            "question": "Welke stelling past het beste bij jou?",
            "answers": [
                {
                    "text": "Je weet wat AI is, maar gebruikt het niet of nauwelijks bewust",
                    "score": 1,
                },
                {
                    "text": "Je gebruikt AI oppervlakkig en soms in je werk, voornamelijk generatieve AI ter ondersteuning van je werkzaamheden",
                    "score": 2,
                },
                {
                    "text": "Je gebruikt AI regelmatig in projecten en je werkzaamheden en hebt mogelijk al geëxperimenteerd met het bouwen van modellen met een ICT-er",
                    "score": 3,
                },
                {
                    "text": "Je hebt veel kennis en kan zelf AI Modellen bouwen",
                    "score": 4,
                },
            ],
        },
        {
            "question_nr": 2,  # Question number
            "question": "Hoe vaak gebruik je in jouw werkzaamheden technologieën als kunstmatige intelligentie?",
            "answers": [
                {"text": "Zelden tot nooit", "score": 1},
                {"text": "Af en toe", "score": 3},
                {"text": "Periodiek", "score": 6},
                {"text": "Dagelijks", "score": 10},
            ],
        },
        {
            "question_nr": 3,  # Question number
            "question": "Hoe schat je jouw eigen kennis en vaardigheid in rond inzet van kunstmatige intelligentie?",
            "answers": [
                {"text": "Ik ben er niet of nauwelijks mee bekend", "score": 1},
                {
                    "text": "Ik ben bekend met de belangrijke concepten en termen van kunstmatige intelligentie",
                    "score": 3,
                },
                {
                    "text": "Ik weet wat generatieve AI is en welke generatieve AI-systemen in zou kunnen gebruiken in mijn werk",
                    "score": 5,
                },
                {
                    "text": "Ik heb generatieve AI-tekstsystemen, beeldgeneratiesystemen of andere generatieve AI-systemen ingezet",
                    "score": 7,
                },
                {
                    "text": "Ik heb enige ervaring met het gebruiken van AI in projecten",
                    "score": 10,
                },
                {
                    "text": "Ik heb ervaring met het bouwen van AI-modellen (alleen of samen met een ICT'er)",
                    "score": 20,
                },
            ],
        },
        {
            "question_nr": 4,  # Question number
            "question": "Kies het onderwerp dat je het meest interesseert:",
            "answers": [
                {"text": "Machinelearning en AI", "topic": "MLAI"},
                {"text": "Data analysis and cleaning", "topic": "DACL"},
                {"text": "AI, ethiek en maatschappelijke gevolgen", "topic": "AIETHIC"},
                {"text": "Generatieve AI & Prompting", "topic": "GENAI"},
            ],
        },
    ]

    # Calculate relevancy points - simplified version
    sorted_courses = calculate_relevancy_points(courses, user_tags)

    return render_template(
        "courses.html",
        courses=sorted_courses,
        user_tags=user_tags,
        all_tags=all_tags,
        quiz_questions=quiz_questions,
    )


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/api/courses")
def get_courses():
    try:
        courses = Course.query.filter_by(status="active").all()
        return jsonify([
            {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "duration": course.duration,
                "status": course.status,
            }
            for course in courses
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/manage_courses", methods=["GET", "POST"])
def manage_courses():
    # Example: Get a specific course by ID
    course_id = request.args.get("course_id")
    course = Course.query.get(course_id) if course_id else None

    courses = Course.query.all()
    tags = Tag.query.all()
    return render_template(
        "manage_courses.html", courses=courses, tags=tags, course=course
    )


@app.route("/manage_users", methods=["GET", "POST"])
def manage_users():
    if request.method == "POST":
        # Handle form submission for adding or editing users
        username = request.form.get("username")
        email = request.form.get("email")
        tags = request.form.get("tags")  # New field for tags

        # Check if we are editing an existing user
        user_id = request.form.get("user_id")
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

        return redirect("/manage_users")  # Redirect to the same page after submission

    # Fetch all users for display
    users = User.query.all()
    return render_template("manage_users.html", users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # Still capture the password input
        # Bypass password verification
        user = User.query.filter_by(username=username).first()
        if user:  # Assume login is successful if the user exists
            session["username"] = username  # Store the username in the session
            return redirect(
                url_for("index")
            )  # Redirect to the homepage or another page
        else:
            # Handle login failure (e.g., show an error message)
            return render_template("login.html", error="User not found")
    return render_template("login.html")  # Render the login template


@app.route("/logout")
def logout():
    session.pop("username", None)  # Verwijder de gebruikersnaam uit de sessie
    return redirect(url_for("index"))  # Redirect naar de hoofdpagina


@app.route("/remove_tag", methods=["POST"])
def remove_tag():
    tag_to_remove = request.form.get("tag")
    user = get_logged_in_user()

    if user and tag_to_remove:
        # Split the tags, remove the specified tag, and update the user
        user_tags = set(user.tags.split())
        user_tags.discard(tag_to_remove)  # Remove the tag if it exists
        user.tags = " ".join(user_tags)  # Rejoin the tags into a string
        db.session.commit()
        return jsonify(success=True, message="Tag removed successfully.")

    return jsonify(success=False, message="Failed to remove tag.")


@app.route("/collect_tags", methods=["POST"])
def collect_tags():
    # Start een database sessie
    with db.session.begin():
        # Haal alle courses op
        courses = Course.query.all()

        # Set om unieke tags op te slaan
        unique_tags = set()

        # Loop door elke course en verzamel tags
        for course in courses:
            if course.tags:
                # Split tags op spaties
                tags = course.tags.split()
                # Voeg elke tag toe aan de set van unieke tags
                unique_tags.update(tags)

        # Voeg unieke tags toe aan de Tags tabel
        for tag_name in unique_tags:
            # Controleer of de tag al bestaat
            existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
            if not existing_tag:
                # Voeg de nieuwe tag toe
                new_tag = Tag(tag_name=tag_name)
                db.session.add(new_tag)

        # Commit de sessie
        try:
            db.session.commit()
            print("Tags succesvol verzameld en toegevoegd.")
        except IntegrityError:
            db.session.rollback()
            print("Er is een fout opgetreden bij het toevoegen van tags.")

    return redirect(url_for("show_collected_tags"))


@app.route("/show_collected_tags")
def show_collected_tags():
    tags = Tag.query.all()
    return render_template("show_collected_tags.html", tags=tags)


@app.route("/save_course", methods=["POST"])
def save_course():
    try:
        # Retrieve form data
        title = request.form.get("title")
        description = request.form.get("description")
        duration = request.form.get("duration")
        status = request.form.get("status")
        tags = request.form.get("tags")

        # Create a new course or update an existing one
        course_id = request.form.get("course_id")
        if course_id:
            # Update existing course
            course = Course.query.get(course_id)
            if course:
                course.title = title
                course.description = description
                course.duration = duration
                course.status = status
                course.tags = tags
        else:
            # Add new course
            new_course = Course(
                title=title,
                description=description,
                duration=duration,
                status=status,
                tags=tags
            )
            db.session.add(new_course)

        # Commit the session
        db.session.commit()
        return redirect(url_for("manage_courses"))
    
    except Exception as e:
        print(f"Error saving course: {str(e)}")  # For debugging
        db.session.rollback()
        return redirect(url_for("manage_courses"))


@app.route("/add_tag", methods=["POST"])
def add_tag():
    tag_to_add = request.form.get("tag")
    user = get_logged_in_user()

    if user and tag_to_add:
        # Split the tags, add the specified tag, and update the user
        user_tags = set(user.tags.split())
        user_tags.add(tag_to_add)  # Add the tag
        user.tags = " ".join(user_tags)  # Rejoin the tags into a string
        db.session.commit()
        return jsonify(success=True, message="Tag added successfully.")

    return jsonify(success=False, message="Failed to add tag.")


@app.route("/edit_tag/<int:tag_id>", methods=["POST"])
def edit_tag(tag_id):
    if session.get("username") == "admin":
        tag_name = request.form.get("tag_name")
        tag = Tag.query.get(tag_id)
        if tag and tag_name:
            tag.tag_name = tag_name
            db.session.commit()
    return redirect(url_for("show_collected_tags"))


@app.route("/delete_tag/<int:tag_id>", methods=["POST"])
def delete_tag(tag_id):
    if session.get("username") == "admin":
        tag = Tag.query.get(tag_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
    return redirect(url_for("show_collected_tags"))


if __name__ == "__main__":
    # Get the port from the environment variable, default to 5000 if not set
    port = int(os.environ.get("PORT", 5001))
    # Run the app on the specified port
    app.run(host="0.0.0.0", port=port, debug=True)
