from app import app, db
from src.models import Course

# Sample course data
courses_data = [
    {
        "title": "Machine Learning Basics",
        "description": "Leer de fundamenten van machine learning en data science. Perfect voor beginners die willen starten met AI en data analyse.",
        "duration": "8 weken",
        "level": "Beginner",
        "status": "active"
    },
    {
        "title": "Python voor Data Analyse",
        "description": "Masterclass in data-analyse met Python en pandas. Leer hoe je data kunt verwerken, analyseren en visualiseren.",
        "duration": "6 weken",
        "level": "Intermediate",
        "status": "active"
    },
    {
        "title": "Deep Learning Advanced",
        "description": "Geavanceerde neural networks en AI-implementaties. Voor ervaren developers die zich willen specialiseren in deep learning.",
        "duration": "10 weken",
        "level": "Advanced",
        "status": "active"
    }
]

with app.app_context():
    # Clear existing courses (optional)
    db.session.query(Course).delete()
    
    # Add new courses
    for course_data in courses_data:
        course = Course(**course_data)
        db.session.add(course)
    
    db.session.commit()  # Commit the changes to the database
    print("Courses added to the database!") 