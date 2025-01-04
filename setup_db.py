from app import app, db  # Adjust the import based on your project structure

with app.app_context():
    # Create all tables
    db.create_all()

    # Check if the admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # Create an admin user
        admin_user = User(username='admin', email='admin@example.com', tags='admin')
        admin_user.set_password('admin')  # Set the password to 'admin'
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

    print("Database and tables created successfully.") 