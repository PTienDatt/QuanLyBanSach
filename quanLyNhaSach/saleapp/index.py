from itertools import product
from saleapp import app, login
from flask import render_template, request, redirect
import dao
from flask import Flask, request, jsonify
from flask_login import login_user, logout_user, current_user
from saleapp import admin

@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    products = dao.load_products(q=q, cate_id=cate_id)
    return render_template('index.html', products=products)


@app.route('/products/<int:id>')
def details(id):
    products = dao.load_product_by_id(id)
    return render_template('product-details.html', products= products)



@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect("/")

    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username, password)
        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "*Tài khoản hoặc mật khẩu không đúng!"
    return render_template('login.html', err_msg=err_msg)



@app.route('/logout', methods=['post'])
def logout():
    logout_user()
    return redirect('/')

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
            dao.add_user(name=name, username=username, password=password, avatar=avatar_path, email=email, address=address, phone=phone)
            return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp!"

    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/product/<int:id>')
def gio_hang(id):
    product = dao.load_product_by_id(id)
    return render_template('GioHang.html', product =product)


@app.route('/ThanhToan')
def mua_hang():
    return render_template('ThanhToan.html')


# @app.route('/product/<int:id>')
# def thanh_toan(id):
#     thanhtoan = dao.load_product_by_id(id)
#     return render_template('GioHang.html', thanhtoan=thanhtoan)


@app.route('/GioHang')
def gio_Hang():
    return render_template('GioHang.html')


@app.context_processor
def common_attributes():
    return {
        "categories": dao.load_categories()
    }


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
