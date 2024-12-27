# saleapp/models.py
import hashlib

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import enum
from datetime import datetime
from saleapp import db, app


class Role(enum.Enum):
    ADMIN = "Admin"
    STAFF = "Staff"
    USER = "User"


class Payment_Method(enum.Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    BANK_TRANSFER = "Bank Transfer"


class Customer(db.Model, UserMixin):  # Tạo bảng Customer
    __tablename__ = 'Customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(255), nullable=False)

    user_role = Column(Enum(Role), default=Role.USER)

    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(255), default='user.png')
    joined_date = Column(String(50), default=datetime.now())
    is_active = Column(Boolean, default=True)
    receipts = db.relationship('Receipt', backref='customer', lazy=True)

    def __str__(self):
        return self.name


class Staff(db.Model):  # Tạo bảng Staff
    __tablename__ = 'Staff'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(255), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(255), default='user.png')
    user_role = Column(db.Enum(Role), default=Role.STAFF)
    import_receipts = db.relationship('ImportReceipt', backref='staff', lazy=True)
    book_managements = db.relationship('BookManagement', backref='staff', lazy=True)

    def __str__(self):
        return self.name



class Category(db.Model):  # Tạo bảng Category
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Author(db.Model):  # Tạo bảng Author
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='author', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):  # Tạo bảng Product
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(255))
    # active= Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    quantity = Column(Integer, default=0)

    receipt_details = db.relationship('ReceiptDetail', backref='product', lazy=True)
    book_managements = db.relationship('BookManagement', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Receipt(db.Model):  # Tạo bảng Receipt
    __tablename__ = 'Receipt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(db.DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    payment_method = Column(db.Enum(Payment_Method), default=Payment_Method.CASH)
    shipping = Column(Boolean, default=False)
    receipt_details = db.relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(db.Model):  # Tạo bảng ReceiptDetail
    __tablename__ = 'ReceiptDetail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    price = Column(Float, default=0, nullable=False)


class ImportReceipt(db.Model):  # Tạo bảng ImportReceipt
    __tablename__ = 'ImportReceipt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_import = Column(db.DateTime, default=datetime.now())
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)
    import_receipt_details = db.relationship('ImportReceiptDetail', backref='import_receipt', lazy=True)


class ImportReceiptDetail(db.Model):  # Tạo bảng ImportReceiptDetail
    __tablename__ = 'ImportReceiptDetail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    import_receipt_id = Column(Integer, ForeignKey(ImportReceipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    price = Column(Float, default=0, nullable=False)
    description = Column(String(255))


class BookManagement(db.Model):  # Tạo bảng BookManagement
    __tablename__ = 'BookManagement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)
    description = Column(String(255), nullable=True)
    date_change = Column(db.DateTime, default=datetime.now())
    quantity = Column(Integer, default=0, nullable=False)
    price = Column(Float, default=0, nullable=False)


def __tr__(self):
    return self.name





if __name__ == "__main__":
    with app.app_context():

        # db.drop_all()   # Drop all table
        #
        # db.create_all()  # Create all table

        # import json
        #
        # # Them du lieu vao bang Category tu file category.json
        # with open(r'C:\QuanLyBanSach\quanLyNhaSach\saleapp\data\categories.json', 'r', encoding='utf-8') as file:
        #     categories = json.load(file)
        #     for cate in categories:
        #         db.session.add(Category(**cate))
        #     db.session.commit()
        #
        # # Them du lieu vao bang Author tu file authors.json
        # with open(r'C:\QuanLyBanSach\quanLyNhaSach\saleapp\data\authors.json', 'r', encoding='utf-8') as file:
        #     authors = json.load(file)
        #     for author in authors:
        #         db.session.add(Author(**author))
        #     db.session.commit()
        #
        # # Them du lieu vao bang Product tu file products.json
        # with app.app_context():
        #     with open(r'C:\QuanLyBanSach\quanLyNhaSach\saleapp\data\products.json', 'r',
        #               encoding='utf-8') as file:
        #         products = json.load(file)
        #         for p in products:
        #             prod = Product(
        #                 name=p['name'].strip(),
        #                 price=float(p['giaCu'].replace('.', '').replace('đ', '').strip()),
        #                 image=p['image'].strip(),
        #                 category_id=p['category_id'],
        #                 author_id=p['author_id']
        #             )
        #             db.session.add(prod)
        #         db.session.commit()

        c = Customer(name="dat", email='dat@gamil.com', phone='0942452345', address='Nhà bè', username='admin',
                     password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), user_role=Role.ADMIN,
                     avatar='https://cdn.pixabay.com/photo/2022/04/08/09/17/frog-7119104_960_720.png', is_active=1)

        db.session.add(c)
        db.session.commit()
