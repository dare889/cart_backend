from models.order import Order, OrderItem
from db import db

from db import db


def create_order(user_id, items, total_price, status='Pending'):
    order = Order(user_id=user_id, total_price=total_price, status=status)
    db.session.add(order)
    db.session.commit()

    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.get('product_id'),
            quantity=item.get('quantity', 0),  # Default quantity to 0 if not provided
            price=item.get('price', 0.0),  # Default price to 0.0 if not provided
        )
        db.session.add(order_item)

    db.session.commit()
    return order


def get_order_by_id(order_id):
    return Order.query.get(order_id)


def get_orders_by_user(user_id):
    return Order.query.filter_by(user_id=user_id).all()


def get_orders_for_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return orders


def get_all_orders():
    orders = Order.query.all()
    return [order.to_dict() for order in orders]