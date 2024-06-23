from flask import Blueprint, request, jsonify
from controllers.product_controller import add_product, get_all_products, get_product_by_id, delete_product
from db import db

product_bp = Blueprint('product', __name__)


@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    print(f"Incoming data: {data}")  # Debugging line

    products = add_product(data)

    response_data = []
    for product in products:
        response_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'original_price': product.original_price,
            'image': product.image,
            'product_type': product.product_type,
            'hot_item': product.hot_item,
            'sub_type': product.sub_type,
            'sku': product.sku
        })

    return jsonify(response_data), 201


@product_bp.route('/', methods=['GET'])
def fetch_all_products():
    products = get_all_products()
    return jsonify([
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'original_price': product.original_price,
            'image': product.image,
            'product_type': product.product_type,  # Updated field name
            'hot_item': product.hot_item,
            'sub_type': product.sub_type,
            'sku': product.sku
        } for product in products
    ])


@product_bp.route('/<int:product_id>', methods=['GET'])
def fetch_product_by_id(product_id):
    product = get_product_by_id(product_id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'original_price': product.original_price,
            'image': product.image,
            'product_type': product.product_type,  # Updated field name
            'hot_item': product.hot_item,
            'sub_type': product.sub_type,
            'sku': product.sku
        })
    return jsonify({'message': 'Product not found'}), 404


@product_bp.route('/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    success = delete_product(product_id)
    if success:
        return jsonify({'message': 'Product deleted successfully'}), 200
    return jsonify({'message': 'Product not found'}), 404


@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = get_product_by_id(product_id)
    if product:
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.original_price = data.get('original_price', product.original_price)
        product.image = data.get('image', product.image)
        product.product_type = data.get('product_type', product.product_type)
        product.hot_item = data.get('hot_item', product.hot_item)
        product.sub_type = data.get('sub_type', product.sub_type)
        product.sku = data.get('sku', product.sku)
        db.session.commit()
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'original_price': product.original_price,
            'image': product.image,
            'product_type': product.product_type,
            'hot_item': product.hot_item,
            'sub_type': product.sub_type,
            'sku': product.sku
        }), 200
    return jsonify({'message': 'Product not found'}), 404
