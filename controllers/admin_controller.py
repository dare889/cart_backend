from models.admin_user import AdminUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from models.order import Order, OrderItem
from models.user import User
from db import db

bcrypt = Bcrypt()

def register_admin_user(username, email, password, admin_type='admin'):
    admin_user = AdminUser(username=username, email=email, password=password, admin_type=admin_type)
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

def get_admin_user_by_id(admin_user_id):
    return AdminUser.query.get(admin_user_id)

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

def get_all_orders():
    orders = Order.query.all()
    return [{
        'id': order.id,
        'user': {'id': order.user.id, 'username': order.user.username},
        'total_price': order.total_price,
        'status': order.status,
        'items': [{
            'id': item.id,
            'product_id': item.product_id,
            'name': item.product.name,  # Get the name from the associated product
            'quantity': item.quantity,
            'price': item.price
        } for item in order.items]
    } for order in orders]

def delete_admin_user(user_id):
    admin_user = AdminUser.query.get(user_id)
    if admin_user:
        db.session.delete(admin_user)
        db.session.commit()
        return True
    return False

def update_admin_user(user_id, data):
    admin_user = AdminUser.query.get(user_id)
    if admin_user:
        admin_user.username = data.get('username', admin_user.username)
        admin_user.email = data.get('email', admin_user.email)
        if 'password' in data:
            admin_user.set_password(data['password'])
        admin_user.admin_type = data.get('admin_type', admin_user.admin_type)
        db.session.commit()
        return admin_user
    return None