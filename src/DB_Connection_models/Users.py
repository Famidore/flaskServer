from run import db


class Users(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    is_premium = db.Column(db.Boolean, nullable=True)
    create_date = db.Column(db.DateTime, nullable=False)
