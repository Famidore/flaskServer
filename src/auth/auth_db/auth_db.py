from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User


def register_user(name, email, password):
    engine = create_engine('sqlite:///../../../dbs/database.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if email already exists declared in database
    existing_email = session.query(User).filter_by(email=email).first()
    if existing_email:
        print("User with this email already exists!")
        return False

    # Add new user to database
    new_user = User(name, email, password)
    session.add(new_user)
    session.commit()
    print("User added successfully.")
    return True

def login_user(name, password):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if user exists
    user = session.query(User).filter_by(name=name).first()
    if user:
        # Check if password is valid
        if user._check_password(password):
            print("User logged correctly.")
            return True
        else:
            print("The password is invalid!")
            return False
    else:
        print("Such user does not exists!")
        return False