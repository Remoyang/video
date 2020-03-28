# coding:utf8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint
# from app import db
app = Flask(__name__)
app.debug = True

# DB init
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@192.168.168.100:30006/movie"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'cb34xxxxxxxxxxxxxxxxxxbae30d90f6'
db = SQLAlchemy(app)

# 导入蓝图
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(home_blueprint)

# 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404

# 500
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('home/500.html'), 500
