from sqlalchemy import Column, Integer, String, Float, Boolean
from db import db

class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    image = Column(String(200))
    product_type = Column(String(50))  # Updated field name
    hot_item = Column(Boolean, default=False)
    sub_type = Column(String(50))

    def __init__(self, name, description, price, original_price, image, product_type, hot_item, sub_type):
        self.name = name
        self.description = description
        self.price = price
        self.original_price = original_price
        self.image = image
        self.product_type = product_type
        self.hot_item = hot_item
        self.sub_type = sub_type
