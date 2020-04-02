# -*- coding: utf8 -*-
import datetime
from . import admin
from flask import render_template, redirect, url_for, flash, request, session
from app.models import Admin, Movie, Tag, Oplog
from forms import LoginForm, MovieForm, TagForm
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import os
import uuid


# 装饰器用来进行访问控制
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 文件名称处理
def change_filename(filename):
    fileinof = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%y%m%d%H%M%S")+str(uuid.uuid4().hex)+fileinof[-1]
    return filename

# 后端首页
@admin.route("/")
def index():
    return render_template("admin/index.html")

# 后端登录
@admin.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash("账号或密码错误! ",'err')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        return redirect(request.args.get('next') or url_for('admin.index'))

    return render_template("admin/login.html", form=form)


# 后端退出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.clear()
    return redirect(url_for("admin.login"))

# 后端修改密码
@admin.route("/pwd/")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")

# 后端添加标签
@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash("名称已经存在！", "err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功！ ", 'OK')
        # oplog = Oplog(
        #     admin_id=session["admin_id"],
        #     ip=request.remote_addr,
        #     reason="添加标签%s" % data["name"]
        # )
        # db.session.add(oplog)
        # db.session.commit()

        return redirect(url_for("admin.tag_add"))

    return render_template("admin/tag_add.html", form=form)

# 后端标签列表
@admin.route("/tag/list/<int:page>/", methods=["GET"])
@admin_login_req
# @admin_auth
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)

# 后端添加电影
@admin.route("/movie/add/", methods=["GET", "POST"])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        # 文件处理
        file_url = secure_filename(form.url.data.filrname)
        file_logo = secure_filename(form.logo.data.filrname)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"]+url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        # 数据处理
        movie = Movie(
            title=data["title"],
            url=url,
            info=data["info"],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=int(data["tag_id"]),
            area=data["release_time"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功！ ", 'OK')
        return redirect(url_for("admin.movie_add"))

    return render_template("admin/movie_add.html", form=form)

# 后端添加电影
@admin.route("/movie/list/")
@admin_login_req
def movie_list():

    return render_template("admin/movie_list.html" )

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