# -*- coding: utf8 -*-
import datetime
from . import admin
from flask import render_template, redirect, url_for, flash, request, session
from app.models import Admin
from forms import LoginForm
from functools import wraps


# 装饰器用来进行访问控制
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

# 后端首页
@admin.route("/")
def index():
    return render_template("admin/index.html")

# 后端登录
@admin.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # print form.account.data
    if form.validate_on_submit():
        data = form.data
        print data
        admin = Admin.query.filter_by(name=data['account']).first()
        print admin
        if not admin.check_pwd(data['pwd']):
            print "111111"
            # flash("密码错误！", 'err')
            flash("账号或密码错误! ",'err')
            return redirect(url_for('admin.login'))
        print 2222
        session['admin'] = data['account']
        return redirect(request.args.get('next') or url_for('admin.index'))

    return render_template("admin/login.html", form=form)


    # form = LoginForm()
    # if form.validate_on_submit():
    #     # data = form.data
    #     # admin = Admin.query.filter_by(name=data['account']).first()
    #     if not admin.check_pwd(data['pwd']):
    #         flash("账号或密码错误! ")
    #         return redirect(url_for('admin.login'))
    #     session['admin'] = data['account']
    #     return redirect((request.args.get('next') or url_for('admin.index')))
    # return render_template('admin/login.html', form=form)

# 后端退出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.clear()
    return redirect(url_for("admin.login"))

# 后端修改密码
@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")

# 后端添加标签
@admin.route("/tag/add/")
def tag_add():
    return render_template("admin/tag_add.html")

# 后端标签列表
@admin.route("/tag/list/")
def tag_list():
    return render_template("admin/tag_list.html")


# 后端添加电影
@admin.route("/movie/add/")
def movie_add():
    return render_template("admin/movie_add.html")

# 后端添加电影
@admin.route("/movie/list/")
def movie_list():
    return render_template("admin/movie_list.html")

# 后端添加预告
@admin.route("/preview/add/")
def preview_add():
    return render_template("admin/preview_add.html")

# 后端预告列表
@admin.route("/preview/list/")
def preview_list():
    return render_template("admin/preview_list.html")

# 后端会员列表
@admin.route("/user/list/")
def user_list():
    return render_template("admin/user_list.html")

# 后端评论列表
@admin.route("/comment/list/")
def comment_list():
    return render_template("admin/comment_list.html")

# 后端收藏列表
@admin.route("/moviecol/list/")
def moviecol_list():
    return render_template("admin/moviecol_list.html")

# 后端操作日志列表
@admin.route("/oplog/list/")
def oplog_list():
    return render_template("admin/oplog_list.html")

# 后端管理员登录日志列表
@admin.route("/adminloginlog/list/")
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")

# 后端管理员登录日志列表
@admin.route("/userloginlog/list/")
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")

# 后端添加权限
@admin.route("/auth/add/")
def auth_add():
    return render_template("admin/auth_add.html")

# 后端权限列表
@admin.route("/auth/list/")
def auth_list():
    return render_template("admin/auth_list.html")

# 后端添加角色
@admin.route("/role/add/")
def role_add():
    return render_template("admin/role_add.html")

# 后端角色列表
@admin.route("/role/list/")
def role_list():
    return render_template("admin/role_list.html")

# 后端添加管理员
@admin.route("/admin/add/")
def admin_add():
    return render_template("admin/admin_add.html")

# 后端管理员列表
@admin.route("/admin/list/")
def admin_list():
    return render_template("admin/admin_list.html")