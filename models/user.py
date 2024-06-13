from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)

    orders = relationship('Order', back_populates='user')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
