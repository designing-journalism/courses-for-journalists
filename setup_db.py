from app import app, db  # Adjust the import based on your project structure

with app.app_context():
    db.create_all()  # This will create all tables defined in your models
    print("Database and tables created!") 