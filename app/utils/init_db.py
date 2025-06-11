from app.models.models import db, User, Tutor, Subject
from werkzeug.security import generate_password_hash

def init_db():
    # Create admin user
    admin = User(
        email='admin@elitetuition.com',
        name='Admin',
        role='admin'
    )
    admin.set_password('admin123')  # Change this in production
    
    # Create subjects
    subjects = [
        Subject(name='Mathematics', description='Mathematics from primary to advanced level', level='All'),
        Subject(name='Physics', description='Physics for secondary and higher secondary', level='Secondary'),
        Subject(name='Chemistry', description='Chemistry for secondary and higher secondary', level='Secondary'),
        Subject(name='Biology', description='Biology for secondary and higher secondary', level='Secondary'),
        Subject(name='English', description='English language and literature', level='All'),
        Subject(name='History', description='World and local history', level='All'),
        Subject(name='Geography', description='Physical and human geography', level='All'),
        Subject(name='Computer Science', description='Programming and computer concepts', level='Secondary'),
        Subject(name='French', description='French language learning', level='All'),
        Subject(name='Music', description='Music theory and practice', level='All')
    ]
    
    # Create sample tutors
    tutors = [
        {
            'email': 'john.doe@example.com',
            'name': 'John Doe',
            'phone': '+1234567890',
            'qualification': 'M.Sc. Mathematics',
            'experience': 5,
            'bio': 'Experienced mathematics tutor with a passion for making complex concepts simple.',
            'subjects': [0, 7]  # Mathematics and Computer Science
        },
        {
            'email': 'jane.smith@example.com',
            'name': 'Jane Smith',
            'phone': '+1234567891',
            'qualification': 'Ph.D. Physics',
            'experience': 8,
            'bio': 'Physics expert specializing in mechanics and quantum physics.',
            'subjects': [1, 2]  # Physics and Chemistry
        }
    ]
    
    try:
        # Add admin
        if not User.query.filter_by(email=admin.email).first():
            db.session.add(admin)
        
        # Add subjects
        for subject in subjects:
            if not Subject.query.filter_by(name=subject.name).first():
                db.session.add(subject)
        
        # Commit to get subject IDs
        db.session.commit()
        
        # Get all subjects for reference
        all_subjects = Subject.query.all()
        
        # Add tutors
        for tutor_data in tutors:
            if not Tutor.query.filter_by(email=tutor_data['email']).first():
                tutor = Tutor(
                    email=tutor_data['email'],
                    name=tutor_data['name'],
                    phone=tutor_data['phone'],
                    qualification=tutor_data['qualification'],
                    experience=tutor_data['experience'],
                    bio=tutor_data['bio'],
                    is_verified=True
                )
                tutor.set_password('tutor123')  # Change this in production
                
                # Add subjects to tutor
                for subject_idx in tutor_data['subjects']:
                    tutor.subjects.append(all_subjects[subject_idx])
                
                db.session.add(tutor)
        
        db.session.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing database: {str(e)}")
        raise 