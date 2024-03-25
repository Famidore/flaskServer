from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import hashlib
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    create_date = Column(DateTime)
    is_premium = Column(Boolean)

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

