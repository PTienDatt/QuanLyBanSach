from math import trunc
from flask import redirect
from urllib3 import request
from saleapp.models import Category, Product, Role
from saleapp import db, app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose, AdminIndexView
import utils
from flask import request
from datetime import datetime
from flask_admin.form import rules


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


admin = Admin(app=app, name='Quản lý bán hàng', template_mode='bootstrap4', index_view=MyAdminIndexView())
# admin.add_view(ModelView(Category, db.session, name="Danh mục"))
# admin.add_view(ProductAdminView(Product, db.session, name="Sản phẩm"))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))

# admin = Admin(app=app, name='Quản lý bán hàng', template_mode='bootstrap4')

admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductAdminView(Product, db.session))
