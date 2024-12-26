from collections import defaultdict
from saleapp import db,app
from saleapp.models import Receipt, ReceiptDetail, Category, Product, Customer
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.sql import extract
import json,os


# Hàm đếm số lượng và tổng tiền trong giỏ hàng
def count_cart(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for p in cart.values():
            total_quantity += p['quantity']
            total_amount += p['quantity'] * p['price']
    return {'total_quantity': total_quantity, 'total_amount': total_amount}

# Hàm thêm hóa đơn vào cơ sở dữ liệu
def add_receipt(cart):
    receipt = Receipt(customer=current_user)
    db.session.add(receipt)
    for c in cart.values():
        d = ReceiptDetail(product_id=c['id'],
                          quantity=c['quantity'],
                          price=c['price'],
                          receipt=receipt)
        db.session.add(d)
    db.session.commit()


# Hàm thống kê số lượng sản phẩm theo danh mục
def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Product.id)) \
        .join(Product,Category.id.__eq__(Product.category_id),isouter=True)  \
        .group_by(Category.id, Category.name).all()


# Hàm thống kê số lượng sản phẩm theo ngày tháng và từ khoa tìm kiếm
# def product_stats(kw=None, from_date=None, to_date=None):
#     p = db.session.query(Product.id, Product.name,
#                          func.sum(ReceiptDetail.quantity * ReceiptDetail.price)) \
#         .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id) , isouter=True) \
#         .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
#         .group_by(Product.id, Product.name)
#     if kw:
#         p= p.filter(Product.name.contains(kw))
#     if from_date:
#         p = p.filter(Receipt.create_date.__ge__(from_date))
#     if to_date:
#         p = p.filter(Receipt.create_date.__le__(to_date))
#
#     return p.all()



def product_stats(kw=None, from_date=None, to_date=None):
    p = db.session.query(Product.id, Product.name,
                         func.sum(ReceiptDetail.quantity * ReceiptDetail.price),

                         func.sum(ReceiptDetail.quantity),
                         func.avg(ReceiptDetail.price)
                         ) \
        .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id), isouter=True)\
        .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id)) \
        .group_by(Product.id, Product.name)

    if kw:
        p = p.filter(Product.name.contains(kw))

    if from_date:
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            p = p.filter(Receipt.create_date >= from_date)
        except ValueError:
            print("Invalid from_date format. Use YYYY-MM-DD.")

    if to_date:
        try:
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
            p = p.filter(Receipt.create_date <= to_date)
        except ValueError:
            print("Invalid to_date format. Use YYYY-MM-DD.")

    return p.all()

# Hàm thống kê số lượng sản phẩm theo tháng
def product_month_stats(year):
    return db.session.query(extract('month', Receipt.create_date),
                            func.sum(ReceiptDetail.quantity * ReceiptDetail.price))\
        .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id))\
        .filter(extract('year', Receipt.create_date) == year)\
        .group_by (extract('month', Receipt.create_date))\
        .order_by(extract('month', Receipt.create_date)).all()














































































