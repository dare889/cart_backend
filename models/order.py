from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from db import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_price = Column(Float, nullable=False)
    # Define relationship with User
    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')
    status = Column(String(50), nullable=False, default='Pending')

    def __init__(self, user_id, total_price, status='Pending'):
        self.user_id = user_id
        self.total_price = total_price
        self.status = status

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_price': self.total_price,
            'status': self.status,
            'items': [item.serialize() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order = relationship('Order', back_populates='items')

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }
