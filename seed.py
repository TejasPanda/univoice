from app import db
from app.models import User, UserRole

def seed_data():
    # Check if an admin already exists
    existing_admin = User.query.filter_by(role=UserRole.ADMIN).first()
    if existing_admin:
        print("Admin already exists. Skipping seed.")
        return

    print("Seeding initial admin account...")

    admin = User(
        email='admin@kiit.ac.in',
        name='Super Admin',
        role=UserRole.ADMIN
    )
    admin.set_password('admin123')

    db.session.add(admin)
    db.session.commit()

    print("Admin created successfully.")