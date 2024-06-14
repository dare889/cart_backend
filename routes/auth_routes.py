from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from controllers.auth_controller import register_user, authenticate_user, get_user_by_id
from models import User
from db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing data'}), 400

    user = register_user(username, email, password)
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'email': user.email})
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user_identity = get_jwt_identity()
    print(f"User identity from JWT: {user_identity}")
    user = get_user_by_id(user_identity['id'])
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200
    return jsonify({'message': 'User not found'}), 404

@auth_bp.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    user_identity = get_jwt_identity()
    username = user_identity['username']
    data = request.get_json()
    user = User.query.filter_by(username=username).first()

    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify({
            'username': user.username,
            'email': user.email
        }), 200
    return jsonify({'message': 'User not found'}), 404