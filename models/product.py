# models/product.py
from db import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    product_type = db.Column(db.String(50), nullable=False)
    hot_item = db.Column(db.Boolean, default=False)
    sub_type = db.Column(db.String(50), nullable=True)
    sku = db.Column(db.String(50), nullable=False, unique=True)
    order_items = db.relationship('OrderItem', back_populates='product')
