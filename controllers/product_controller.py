from models.product import Product
from db import db

def add_product(data):
    if isinstance(data, list):
        new_products = []
        for product_data in data:
            new_product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                original_price=product_data['original_price'],
                image=product_data['image'],
                product_type=product_data['product_type'],
                hot_item=product_data['hot_item'],
                sub_type=product_data['sub_type']
            )
            new_products.append(new_product)
            db.session.add(new_product)
        db.session.commit()
        return new_products
    else:
        new_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            original_price=data['original_price'],
            image=data['image'],
            product_type=data['product_type'],
            hot_item=data['hot_item'],
            sub_type=data['sub_type']
        )
        db.session.add(new_product)
        db.session.commit()
        return [new_product]

def get_all_products():
    return Product.query.all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return True
    return False
