import csv
from app import app, db
from src.models import Course

# Path to the CSV file
csv_file_path = 'data/Elearnings.csv'

# Confirmation prompt
confirmation = input("Are you sure? Going on will change the courses known in the database. (yes/no): ")
if confirmation.lower() != 'yes':
    print("Operation cancelled.")
    exit()

with app.app_context():
    # Clear existing courses
    db.session.query(Course).delete()
    
    # Open the CSV file and read its contents
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # Use ';' as the delimiter
        for row in reader:
            # Create a new Course instance from the CSV row
            course = Course(
                title=row['Titel'],
                description=row['Beschrijving'],
                duration=row['Tijdsinvestering'],
                level=row['Niveau'],
                status='active'  # Set status to 'active' by default
            )
            db.session.add(course)  # Add the course to the session

    db.session.commit()  # Commit the changes to the database
    print("Existing courses deleted and new courses imported from CSV to the database!") 