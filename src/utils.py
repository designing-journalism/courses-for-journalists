from flask import session
from src.models import User

def calculate_relevancy_points(user, courses, search_text, level, quiz_answers):
    """
    Calculate relevancy points for each course based on user info, search criteria, and quiz answers.

    :param user: The logged-in user object.
    :param courses: A list of course objects.
    :param search_text: Text from the search bar.
    :param level: Selected level from the combo-box.
    :param quiz_answers: Selected answers from the quiz questions.
    :return: A list of courses sorted by relevancy points.
    """
    relevancy_scores = []

    for course in courses:
        score = 0

        # Example scoring logic
        if search_text.lower() in course.title.lower() or search_text.lower() in course.description.lower():
            score += 10

        if level == course.level:
            score += 5

        # Add more logic based on quiz_answers and user preferences
        # For example, if the user has a preference for certain tags
        if user.tags and course.tags:
            user_tags = set(user.tags.split())
            course_tags = set(course.tags.split())
            score += len(user_tags.intersection(course_tags)) * 2

        # Add score to the list
        relevancy_scores.append((course, score))

    # Sort courses by score in descending order
    relevancy_scores.sort(key=lambda x: x[1], reverse=True)

    # Return sorted courses
    return [course for course, score in relevancy_scores] 

def get_logged_in_user():
    # Assuming the username is stored in the session
    username = session.get('username')
    if username:
        # Query the database to get the user object
        user = User.query.filter_by(username=username).first()
        return user
    return None 