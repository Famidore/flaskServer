from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    create_date = db.Column(db.DateTime)
    is_premium = db.Column(db.Boolean)

    def __init__(self, name, email, password):
        self.name = name
        self.password = self._hash_password(password)
        self.email = email
        self.create_date = datetime.now()
        self.is_premium = False

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _check_password(self, password):
        return self.password == self._hash_password(password)

class Moderator(db.Model):
    __tablename__ = "moderators"

    moderator_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

class PremiumUser(db.Model):
    __tablename__ = "premium_users"

    premium_user_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # Categories checkboxes (Boolean)