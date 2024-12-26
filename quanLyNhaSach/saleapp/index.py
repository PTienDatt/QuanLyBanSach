from itertools import product
from statistics import quantiles
import utils
from saleapp import app, login, db
from flask import render_template, request, redirect, abort, session, jsonify, url_for
from flask import render_template, request, redirect, abort, session
import dao
from flask import Flask, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from saleapp import admin
import cloudinary.uploader
from saleapp.models import *
import random
from saleapp.utils import count_cart



# Trang chu
@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    products = dao.load_products(q=q, cate_id=cate_id)
    return render_template('index.html', products=products)


# Xem chi tiet san pham
@app.route('/products/<int:id>')
def details(id):
    products = db.session.query(Product, Author).join(Author, Product.author_id == Author.id).filter(
        Product.id == id).first()
    if products is None:
        abort(404)
    random_pages = random.randint(150, 500)
    return render_template('product-details.html', products=products, random_pages=random_pages)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login_my_user():
    err_msg = ""
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        user = None
        if role == 'staff':
            role = Role.STAFF
            user = dao.auth_user(username, password, role=role)
        elif role == 'admin':
            role = Role.ADMIN
            user = dao.auth_user(username, password, role=role)
        else:
            role = Role.USER
            user = dao.auth_user(username, password, role=role)
        if user:
            login_user(user=user)

            return redirect('/admin' if role in [Role.STAFF, Role.ADMIN] else '/')
        else:
            err_msg = "*Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)


# Log.out
@app.route('/logout', methods=['post'])
def logout():
    logout_user()
    return redirect('/')


# Đăng ký
@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.__eq__(confirm):
            username = request.form.get("username")
            name = request.form.get("name")
            avatar = request.files.get('avatar')
            avatar_path = None
            email = request.form.get('email')
            address = request.form.get('address')
            phone = request.form.get('phone')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']
            dao.add_user(name=name, username=username, password=password, avatar=avatar_path, email=email,
                         address=address, phone=phone)
            return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp!"

    return render_template('register.html', err_msg=err_msg)





# Cập nhật giỏ hàng
@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    cart = session.get('cart')
    if not cart:
        cart = {}
    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {'id': id, 'name': name, 'price': price, 'quantity': 1}
    session['cart'] = cart

    import utils
    return jsonify(utils.count_cart(cart))


# Xem giỏ hàng
@app.route('/cart')
def cart():
    return render_template('cart.html',
                           stats=utils.count_cart(session.get('cart')))


# Thanh Toán
@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})
    return jsonify({'code': 200})


@app.context_processor
def common_attributes():
    return {
        "categories": dao.load_categories()
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.context_processor
def comment_respone():
    return {
        "cart_stats": utils.count_cart(session.get('cart'))
    }


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
