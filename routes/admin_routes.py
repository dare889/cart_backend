from flask import Blueprint, request, jsonify
from models.admin_user import AdminUser
from controllers.admin_controller import create_admin_user, authenticate_admin, register_admin_user, \
    authenticate_admin_user, update_admin_password, get_all_admin_users, get_admin_user_by_id, delete_admin_user, \
    update_admin_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from controllers.admin_controller import get_all_orders

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/setup', methods=['POST'])
def setup_first_admin():
    # existing_super_admin = AdminUser.query.filter_by(admin_type='super_admin').first()
    # if existing_super_admin:
    #     return jsonify({"message": "Super admin already exists"}), 400

    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_super_admin = create_admin_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        admin_type='super_admin'
    )
    return jsonify({
        'id': new_super_admin.id,
        'username': new_super_admin.username,
        'email': new_super_admin.email,
        'admin_type': new_super_admin.admin_type
    }), 201

@admin_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    data = request.get_json()
    current_user = get_jwt_identity()
    if current_user['admin_type'] not in ['super_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    new_admin = register_admin_user(data['username'], data['email'], data['password'], data.get('admin_type', 'super_admin'))
    return jsonify({
        'id': new_admin.id,
        'username': new_admin.username,
        'email': new_admin.email,
        'admin_type': new_admin.admin_type
    }), 201

@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    admin_user = authenticate_admin_user(username, password)
    if not admin_user:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={
        'id': admin_user.id,
        'username': admin_user.username,
        'email': admin_user.email,
        'admin_type': admin_user.admin_type
    })
    return jsonify({'access_token': access_token}), 200

@admin_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    current_user = get_jwt_identity()
    if current_user['admin_type'] not in ['super_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    updated_admin = update_admin_password(current_user['id'], data['new_password'])
    if updated_admin:
        return jsonify({'message': 'Password updated successfully'}), 200
    return jsonify({'message': 'Failed to update password'}), 400

@admin_bp.route('/admin_users', methods=['GET'], endpoint='list_admin_users')
@jwt_required()
def list_admin_users():
    current_user = get_jwt_identity()
    if current_user['admin_type'] not in ['super_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    admins = get_all_admin_users()
    return jsonify([{
        'id': admin.id,
        'username': admin.username,
        'email': admin.email,
        'admin_type': admin.admin_type
    } for admin in admins]), 200

@admin_bp.route('/admin_users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_admin(user_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    if current_user['admin_type'] not in ['super_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    updated_admin = update_admin_user(user_id, data)
    if updated_admin:
        return jsonify(updated_admin.serialize()), 200
    return jsonify({'message': 'Failed to update admin user'}), 400

@admin_bp.route('/admin_users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_admin(user_id):
    current_user = get_jwt_identity()
    if current_user['admin_type'] not in ['super_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    success = delete_admin_user(user_id)
    if success:
        return jsonify({'message': 'Admin user deleted successfully'}), 200
    return jsonify({'message': 'Failed to delete admin user'}), 400


@admin_bp.route('/detail', methods=['GET'])
@jwt_required()
def get_admin_user():
    current_user = get_jwt_identity()
    admin_user = AdminUser.query.get(current_user['id'])
    if admin_user:
        return jsonify({
            'id': admin_user.id,
            'username': admin_user.username,
            'email': admin_user.email,
            'admin_type': admin_user.admin_type
        }), 200
    return jsonify({'message': 'User not found'}), 404


@admin_bp.route('/orders', methods=['GET'])
def fetch_all_orders():
    orders = get_all_orders()
    return jsonify(orders), 200

@admin_bp.route('/admin_users/<int:admin_user_id>', methods=['GET'], endpoint='get_admin_user_by_id')
@jwt_required()
def get_admin_user(admin_user_id):
    current_user = get_jwt_identity()
    if current_user['admin_type'] not in ['super_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    admin_user = get_admin_user_by_id(admin_user_id)
    if admin_user:
        return jsonify({
            'id': admin_user.id,
            'username': admin_user.username,
            'email': admin_user.email,
            'admin_type': admin_user.admin_type
        }), 200
    return jsonify({'message': 'Admin user not found'}), 404