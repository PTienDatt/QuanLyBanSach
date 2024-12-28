import json
from flask import jsonify, request
from itertools import product
from saleapp import db
from saleapp.models import *
from fuzzywuzzy import process  # thư viện tìm kiêm lấy kết quả gần nhất
from unidecode import unidecode  # thư viện tìm kếm ko cần bỏ dấu
import hashlib


def load_categories():
    with open('data/categories.json', encoding='utf-8') as f:
        return json.load(f)


def load_categories2():
    with open('data/categories2.json', encoding='utf-8') as f:
        return json.load(f)


def load_products(q=None, cate_id=None):
    # with open('data/products.json', encoding='utf-8') as f:
    #     products = json.load(f)
    #    # không phân biệt ch hoa chữ thuường
    #     if q:
    #         products = [p for p in products if q.lower() in p["name"].lower()]
    #
    #     if q:
    #         # Tìm các sản phẩm có tên gần giống với từ khóa tìm kiếm
    #         product_names = [product['name'] for product in products]
    #         matches = process.extract(q, product_names, limit=5)  # Lấy 5 kết quả gần nhất
    #
    #         # Tìm các sản phẩm có tên gần giống với kết quả trả về từ fuzzywuzzy
    #         result = []
    #         for match in matches:
    #             # Tìm sản phẩm tương ứng với tên gần đúng
    #             matched_product = next((product for product in products if product['name'] == match[0]), None)
    #             if matched_product:
    #                 result.append(matched_product)
    #     else:
    #         result = []
    #     if cate_id:
    #         products = [p for p in products if p["category_id"].__eq__(int(cate_id))]
    #     return products
    query = db.session.query(Product)

    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))

    if cate_id:
        query = query.filter(Product.category_id == cate_id)

    products = query.all()

    if q:
        product_names = [product.name for product in products]
        matches = process.extractWithoutOrder(q, product_names)  # Use extractWithoutOrder
        result = []
        for match in matches:
            matched_product = next((product for product in products if product.name == match[0]), None)
            if matched_product:
                result.append(matched_product)
        return result

    return products


def add_user(name, username, password, avatar, email, address, phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = None
    if avatar:
        u = Customer(name=name, username=username, password=password, avatar=avatar, email=email, address=address,
                     phone=phone)
    else:
        u = Customer(name=name, username=username, password=password, email=email, address=address, phone=phone)
    db.session.add(u)
    db.session.commit()

def add_staff(name, username, password, avatar, email, address, phone, role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = None
    if avatar:
        u = Staff(name=name, username=username, password=password, avatar=avatar, email=email, address=address,
                     phone=phone, user_role=role)
    else:
        u = Staff(name=name, username=username, password=password, email=email, address=address, phone=phone, user_role=role)
    db.session.add(u)
    db.session.commit()


def auth_user(username, password, role=Role.USER):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return Customer.query.filter(Customer.username.__eq__(username),
                                 Customer.password.__eq__(password),
                                 Customer.user_role.__eq__(role)).first()


def auth_staff(username, password, role):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return Staff.query.filter(Staff.username.__eq__(username),
                              Staff.password.__eq__(password),
                              Staff.user_role.__eq__(role)).first()


def load_product_by_id(id):
    # with open('data/products.json', encoding='utf-8') as f:
    #     products = json.load(f)
    #     for p in products:
    #         if p["id"] == id:
    #             return p
    product = db.session.query(Product).filter(Product.id == id).first()
    if product:
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "image": product.image,
            "category_id": product.category_id,
            "author_id": product.author_id,
            "quantity": product.quantity
        }
    return None


def get_user_by_id(user_id):
    user = Customer.query.get(user_id) or Staff.query.get(user_id)
    return user


if __name__ == "__main__":
    print(load_products())
