from app import app, db
from src.models import Course

with app.app_context():
    # Query all courses
    courses = Course.query.all()
    
    # Check if any courses were found
    if not courses:
        print("No courses found in the database.")
    else:
        print(f"Found {len(courses)} course(s):")
        for course in courses:
            print(f"ID: {course.id}, Title: {course.title}, Description: {course.description}, Duration: {course.duration}, Level: {course.level}, Status: {course.status}")