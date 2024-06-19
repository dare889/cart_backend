# models/admin_user.py

from db import db
from sqlalchemy import Column, Integer, String, Enum
from werkzeug.security import check_password_hash

class AdminUser(db.Model):
    __tablename__ = 'admin_users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    admin_type = Column(Enum('super_admin', 'admin'), nullable=False)

    def __init__(self, username, email, password, admin_type):
        self.username = username
        self.email = email
        self.password = password
        self.admin_type = admin_type

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'admin_type': self.admin_type
        }
