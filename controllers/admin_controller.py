from models.admin_user import AdminUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from db import db

bcrypt = Bcrypt()

def register_admin_user(username, email, password, admin_type='admin'):
    admin_user = AdminUser(username=username, email=email, admin_type=admin_type)
    admin_user.set_password(password)
    db.session.add(admin_user)
    db.session.commit()
    return admin_user

def authenticate_admin_user(username, password):
    admin_user = AdminUser.query.filter_by(username=username).first()
    if admin_user and admin_user.check_password(password):
        return admin_user
    return None

def get_admin_user_by_id(admin_user_id):
    return AdminUser.query.get(admin_user_id)

def update_admin_password(admin_user_id, new_password):
    admin_user = AdminUser.query.get(admin_user_id)
    if admin_user:
        admin_user.set_password(new_password)
        db.session.commit()
        return admin_user
    return None

def get_all_admin_users():
    return AdminUser.query.all()

def create_admin_user(username, email, password, admin_type):
    hashed_password = generate_password_hash(password)
    new_admin_user = AdminUser(
        username=username,
        email=email,
        password=hashed_password,
        admin_type=admin_type
    )
    db.session.add(new_admin_user)
    db.session.commit()
    return new_admin_user

def authenticate_admin(username, password):
    admin = AdminUser.query.filter_by(username=username).first()
    if admin and check_password_hash(admin.password, password):
        return admin
    return None
