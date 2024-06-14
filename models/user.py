from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'
