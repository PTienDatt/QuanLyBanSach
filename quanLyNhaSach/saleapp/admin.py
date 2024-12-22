from math import trunc
from saleapp.models import Category, Product
from saleapp import db,app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class ProductAdminView(ModelView):
    column_searchable_list = ['name','price' ]
    column_filters = ['name','price']
    can_view_details = True
    can_export = True
    column_exclude_list = ['description','quantity']
    column_labels = {
        'name': 'Tên sản phẩm',
        'price': 'Giá',
        'category_id': 'Danh mục',
        'image': 'Ảnh'
    }

admin = Admin(app= app, name='Quản lý bán hàng', template_mode='bootstrap4')
admin.add_view(ModelView(Category, db.session, name="Danh mục"))
admin.add_view(ProductAdminView(Product, db.session, name="Sản phẩm"))
