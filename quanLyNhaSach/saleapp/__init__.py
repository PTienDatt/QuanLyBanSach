from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/quanlybansach?charset=utf8mb4" % quote('123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


@app.template_filter('format_vnd') # Định dạng tiền tệ
def format_vnd(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except ValueError:
        return value