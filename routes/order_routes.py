from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.order_controller import create_order, get_order_by_id, get_orders_by_user, get_orders_for_user

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order_route():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    items = data.get('items')
    total_price = data.get('total_price')
    status = data.get('status', 'Pending') # Default status to 'Pending' if not provided

    order = create_order(user_id, items, total_price, status)
    return jsonify({'message': 'Order created successfully', 'order': order.serialize()}), 201

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_route(order_id):
    order = get_order_by_id(order_id)
    if order:
        return jsonify(order.serialize()), 200
    return jsonify({'message': 'Order not found'}), 404

@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def list_orders_route():
    user_id = get_jwt_identity()['id']
    orders = get_orders_by_user(user_id)
    return jsonify([order.serialize() for order in orders]), 200


@order_bp.route('/orders', methods=['PUT'])
@jwt_required()
def update_order_status():
    data = request.get_json()
    order_id = data.get('order_id')
    status = data.get('status')

    order = get_order_by_id(order_id)
    if order:
        order.status = status
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully', 'order': order.serialize()}), 200
    return jsonify({'message': 'Order not found'}), 404