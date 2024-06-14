from models.user import User
from db import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def register_user(username, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Using bcrypt for hashing
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"User found: {user.username}, Hash: {user.password}")
    else:
        print("User not found")

    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None


def get_user_by_id(user_id):
    return User.query.get(user_id)
