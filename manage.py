# codeing:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
# 连接数据库
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:123456@192.168.168.100:30006/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db=SQLAlchemy(app)

# 定义数据库表
# 用户表
class User(db.Model):
    __tbalename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtim = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uuid = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return "<User %r>" % self.name

# 用户日志表
class Userlog(db.Model):
    __import__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey("user_id"))
    ip =db.Column(db.String(100))
    addtime =db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<UserLog %r>" % self.id


if __name__ == '__main__':
    app.run()