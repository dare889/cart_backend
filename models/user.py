from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    orders = relationship('Order', back_populates='user')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }



