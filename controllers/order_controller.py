from models.order import Order, OrderItem
from db import db


def create_order(user_id, items, total_price):
    order = Order(user_id=user_id, total_price=total_price)
    db.session.add(order)
    db.session.commit()

    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )
        db.session.add(order_item)

    db.session.commit()
    return order


def get_order_by_id(order_id):
    return Order.query.get(order_id)


def get_orders_by_user(user_id):
    return Order.query.filter_by(user_id=user_id).all()
