from math import trunc
from flask import redirect, flash
from urllib3 import request
from saleapp.models import *
from saleapp import db, app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose, AdminIndexView
import utils
from flask import request
from datetime import datetime
from flask_admin.form import rules
import dao
import cloudinary.uploader


# Hiển thị sản phẩm
class ProductAdminView(ModelView):
    column_searchable_list = ['name', 'price']
    column_filters = ['name', 'price']
    can_view_details = True
    can_export = True
    column_exclude_list = ['description', 'quantity']
    column_labels = {
        'name': 'Tên sản phẩm',
        'price': 'Giá',
        'category_id': 'Danh mục',
        'author_id': 'Tác giả',
        'image': 'Ảnh'
    }


# Đăng xuất
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


# Trang chủ admin
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.category_stats())


# Thống kê
class StatsView(BaseView):
    @expose('/')
    def index(self, ):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/stats.html',
                           month_stats=utils.product_month_stats(year=year),
                           stats=utils.product_stats(kw=kw),
                           from_date=from_date,
                           to_date=to_date
                           )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == Role.ADMIN

class ManageRuleView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def manage_view(self):
        rule = ManageRule.query.first()  # Lấy quy định đầu tiên (vì có thể chỉ cần một bản ghi)

        if request.method == 'POST':  # Nếu phương thức là POST, cập nhật quy định
            import_quantity_min = int(request.form.get('import_quantity_min', 0))
            quantity_min = int(request.form.get('quantity_min', 0))
            cancel_time = int(request.form.get('cancel_time', 0))

            if not rule:  # Nếu chưa tồn tại quy định, tạo mới
                rule = ManageRule(
                    import_quantity_min=import_quantity_min,
                    quantity_min=quantity_min,
                    cancel_time=cancel_time,
                    updated_date=datetime.now()
                )
                db.session.add(rule)
            else:  # Cập nhật quy định hiện có
                rule.import_quantity_min = import_quantity_min
                rule.quantity_min = quantity_min
                rule.cancel_time = cancel_time
                rule.updated_date = datetime.now()

            db.session.commit()
            flash("Cập nhật quy định thành công!", "success")
            # return self.render('admin/manage_rules.html')

        return self.render('admin/ManageRule.html', rule=rule)

class AddStaffView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def add_staff(self):
        err_msg = ''
        if request.method == 'POST':
            password = request.form.get('password')
            confirm = request.form.get('confirm')

            if password.__eq__(confirm):
                name = request.form.get('name')
                username = request.form.get('username')
                password = request.form.get('password')
                avatar = request.files.get('avatar')
                avatar_path = None
                email = request.form.get('email')
                address = request.form.get('address')
                phone = request.form.get('phone')
                role = request.form.get('user_role')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                if role == 'STAFF':
                    dao.add_staff(name=name, username=username, password=password, avatar=avatar_path, email=email, phone = phone,
                                  address=address, role=Role.STAFF)
                else:
                    dao.add_staff(name=name, username=username, password=password, avatar=avatar_path, email=email, phone = phone,
                                  address=address, role=Role.MANAGER)
                err_msg = 'Thêm tài khoản thành công !!!'
            else:
                err_msg = 'Mật khẩu không khớp!'

        return self.render('admin/add_staff.html', err_msg=err_msg)


admin = Admin(app=app, name='Quản lý bán hàng', template_mode='bootstrap4', index_view=MyAdminIndexView())
# admin.add_view(ModelView(Category, db.session, name="Danh mục"))
# admin.add_view(ProductAdminView(Product, db.session, name="Sản phẩm"))
admin.add_view(StatsView(name='Thống kê'))
# admin = Admin(app=app, name='Quản lý bán hàng', template_mode='bootstrap4')   b
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductAdminView(Product, db.session))
admin.add_view(ManageRuleView(name='Quy định'))
admin.add_view(AddStaffView(name='Thêm nhân viên'))
admin.add_view(LogoutView(name='Đăng xuất'))
