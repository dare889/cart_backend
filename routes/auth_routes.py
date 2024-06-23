from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from controllers.auth_controller import register_user, authenticate_user, get_user_by_id
from models.user import User
from db import db

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = register_user(data['username'], data['email'], data['password'])
    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = authenticate_user(username, password)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'email': user.email})
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user_identity = get_jwt_identity()
    user = get_user_by_id(user_identity['id'])
    return jsonify({
        'username': user.username,
        'email': user.email
    }), 200

@auth_bp.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    user_identity = get_jwt_identity()
    username = user_identity['username']
    data = request.get_json()
    user = User.query.filter_by(username=username).first()

    if user:
        if 'email' in data:
            user.email = data['email']
        if 'password' in data and data['password']:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        db.session.commit()
        return jsonify({
            'username': user.username,
            'email': user.email
        }), 200
    return jsonify({'message': 'User not found'}), 404

