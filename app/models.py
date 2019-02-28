# codeing:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
# 连接数据库
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:123456@192.168.168.100:30006/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db=SQLAlchemy(app)

# 定义数据库表
# 会员表
class User(db.Model):
    __tbalename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtim = db.Column(db.DateTime, index=True, default=datetime.now())
    uuid = db.Column(db.String(255), unique=True)
    userlogs = db.relationship('Userlog', backerf='user') # 会员日志外键关系
    comments = db.relationship('Comment', backerf='user')  # 评论外键关系
    moviecols = db.relationship('Moviecol', backerf='user')  # 评论外键关系
    def __repr__(self):
        return "<User %r>" % self.name

# 会员日志表
class Userlog(db.Model):
    __import__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey("user.id"))
    ip =db.Column(db.String(100))
    addtime =db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<UserLog %r>" % self.id

# 标签
class Tag(db.Model):
    __import__ = "tag"
    id = db.Column(db.Integer, primary_key=True) # 编号
    name = db.Column(db.String(100), unique=True) # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) #添加时间
    movies = db.relationship("Movie", backref='tag')

    def __repr__(self):
        return "<Tag %r>" % self.name

# 电影
class Movie(db.Model):
    __import__ = "movie"
    id = db.Column(db.Integer, primary_key=True) # 编号
    title =db.Column(db.String(255), unique=True) # 标题
    url = db.Column(db.String(255), unique=True) # 地址
    info = db.Column(db.Text) # 简介
    logo = db.Column(db.String(255), unique=True) # 封面
    star = db.Column(db.SmallInteger) # 星级
    playnum = db.Column(db.BigInteger) # 播放量
    commentnum = db.Column(db.BigInteger) # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id')) # 所属标签
    area = db.Column(db.String(255)) # 上映地区
    release_time = db.Column(db.Date) # 上映时间
    length = db.Column(db.String(100)) # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) #添加时间
    comments = db.relationship('Comment', backerf='movie')  # 评论外键关系
    moviecols = db.relationship('Moviecol', backerf='movie')  # 电影收藏外键关系

    def __repr__(self):
        return "<Movie %r>" % self.title

# 上映预告
class Preview(db.Model):
    __import__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title

# 评论
class Comment(db.Model):
    __import__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text) # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id

# 电影收藏
class Moviecol(db.Model):
    __import__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Moviecols %r>" % self.id

# 权限
class Auth(db.Model):
    __import__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True) # 名称
    url = db.Column(db.String(255), unique=True) # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name

# 角色
class Role(db.Model):
    __import__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600)) # 角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship('Admin', backerf='role')  # 管理员外键关系

    def __repr__(self):
        return "<Role %r>" % self.name

# 管理员
class Admin(db.Model):
    __tbalename__ = "admin"
    id = db.Column(db.Integer, primary_key=True) # 编号
    name = db.Column(db.String(100), unique=True) # 管理员账号
    pwd = db.Column(db.String(100)) # 管理员密码
    is_super = db.Column(db.SmallInteger) # 是否为超级管理员 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    Adminlogs = db.relationship('Adminlog', backerf='admin')  # 管理员登陆日志外键关系
    oplogs = db.relationship('Oplog', backerf='admin')  # 管理员登陆日志外键关系

    def __repr__(self):
        return "<Admin %r>" % self.name

# 管理员登陆日志
class Adminlog(db.Model):
    __import__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id")) # 所属管理员
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Adminlog %r>" % self.id

#操作日志
class Oplog(db.Model):
    __import__ = "oplog"
    id = db.Column(db.Integer, primary_key=True) # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id")) # 所属管理员
    ip = db.Column(db.String(100))  # 登陆IP
    reason = db.Column(db.String(600)) # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) # 添加时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == '__main__':
    # 1.创建数据库
    # db.create_all()  # 创建数据库时打开 会创建上面列举的表

    # 2.插入数据
    #这里插入一条角色的数据
    """
     role = Role(
        name="超级管理员",
        auths="0")
    db.session.add(role)
    db.session.commit()
    """

    #3.插入一条管理员数据

    from werkzeug.security import generate_password_hash  # 导入生成密码的工具

    admin = Admin(
        namr = "zhiyun",
        pwd = generate_password_hash("123456"),
        is_super = 0,
        role_id = 1

    )
    db.session.add(admin)
    db.session.commit()