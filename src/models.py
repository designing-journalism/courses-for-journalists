from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')  # 'active' or 'inactive'
    tags = db.Column(db.String(255))  # New field for tags
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @property
    def tag_list(self):
        """Convert tags string to list"""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Store hashed passwords
    tags = db.Column(db.String(255))  # New field for tags
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    rating = db.Column(db.Integer)  # e.g., 1 to 5
    feedback = db.Column(db.Text)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    answer_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# New Tag model
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Tag(tag_name='{self.tag_name}')>"
