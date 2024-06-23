# routes/user_routes.py

from flask import Blueprint, jsonify, request

from models.order import Order
from models.user import User
from db import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize()), 200
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@user_bp.route('/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    user = User.query.get(user_id)
    if user:
        orders = Order.query.filter_by(user_id=user_id).all()
        return jsonify([order.serialize() for order in orders]), 200
    return jsonify({'message': 'User not found'}), 404