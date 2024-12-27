import socketio
from flask import Flask, render_template,session,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager, current_user
import secrets
import cloudinary


app = Flask(__name__)


app.secret_key = "project12345@@"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/quanlybansach?charset=utf8mb4" % quote('123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True



db = SQLAlchemy(app=app)
login = LoginManager(app)

cloudinary.config(
    cloud_name='dulpttl26',
    api_key='918116311519748',
    api_secret='XrRTrrc0G5u823Ehmkzh8iuWVOU'
)

@app.template_filter('format_vnd') # Định dạng tiền tệ
def format_vnd(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except ValueError:
        return value
