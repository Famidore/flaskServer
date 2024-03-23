from ..models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def register_user(name, email, password):
    engine = create_engine('sqlite:///../../dbs/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if email already exists declared in database
    existing_email = Session.query(User).filter_by(email=email).first()
    if existing_email:
        print("User with this email already exists!")
        return False

    # Add new user to database
    new_user = User(name, email, password)
    session.add(new_user)
    session.commit()
    print("User added successfully.")
    return True
