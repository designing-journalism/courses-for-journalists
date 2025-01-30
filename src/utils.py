from flask import session
from src.models import User

def calculate_relevancy_points(courses, user_tags, *args):
    """Calculate relevancy points for each course based on matching tags"""
    courses_with_points = []
    
    for course in courses:
        points = 0
        course_tags = course.tag_list
        
        # Add points for matching tags
        for tag in user_tags:
            if tag in course_tags:
                points += 1
                
        courses_with_points.append((course, points))
    
    # Sort courses by points (highest first)
    sorted_courses = sorted(courses_with_points, key=lambda x: x[1], reverse=True)
    return [course for course, _ in sorted_courses]

def get_logged_in_user():
    # Assuming the username is stored in the session
    username = session.get('username')
    if username:
        # Query the database to get the user object
        user = User.query.filter_by(username=username).first()
        return user
    return None 