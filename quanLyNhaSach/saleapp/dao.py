import json,jsonify, request
from itertools import product

from fuzzywuzzy import process     # thư viện tìm kiêm lấy kết quả gần nhất
from unidecode import unidecode    # thư viện tìm kếm ko cần bỏ dấu


def load_categories():
    with open('data/categories.json', encoding='utf-8') as f:
        return json.load(f)


def load_categories2():
    with open('data/categories2.json', encoding='utf-8') as f:
        return json.load(f)




def load_products(q=None, cate_id=None):
    with open('data/products.json', encoding='utf-8') as f:
        products = json.load(f)


       # không phân biệt ch hoa chữ thuường
        if q:
            products = [p for p in products if q.lower() in p["name"].lower()]

        if q:
            # Tìm các sản phẩm có tên gần giống với từ khóa tìm kiếm
            product_names = [product['name'] for product in products]
            matches = process.extract(q, product_names, limit=5)  # Lấy 5 kết quả gần nhất

            # Tìm các sản phẩm có tên gần giống với kết quả trả về từ fuzzywuzzy
            result = []
            for match in matches:
                # Tìm sản phẩm tương ứng với tên gần đúng
                matched_product = next((product for product in products if product['name'] == match[0]), None)
                if matched_product:
                    result.append(matched_product)
        else:
            result = []
        if cate_id:
            products = [p for p in products if p["category_id"].__eq__(int(cate_id))]
        return products


def load_product_by_id(id):
    with open('data/products.json', encoding='utf-8') as f:
        products = json.load(f)
        for p in products:
            if p["id"] == id:
                return p


if __name__ == "__main__":
    print(load_products())
