# coding:utf8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# DB init
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@10.71.70.129:3306/movie"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'cb34xxxxxxxxxxxxxxxxxxbae30d90f6'
# 上传文件保存路径
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")

# app init
app.debug = True
db = SQLAlchemy(app)

# 导入蓝图
from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(home_blueprint)

# 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404

# 500
# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('home/500.html'), 500
