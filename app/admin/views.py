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
        flash("添加标签成功！ ", 'info')

        return redirect(url_for("admin.tag_add"))

    return render_template("admin/tag_add.html", form=form)

# 后端标签列表
@admin.route("/tag/list/<int:page>/", methods=["GET"])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)

# 后端标签编辑
@admin.route("/tag/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(int(id))
    # 如果是请求的话填充信息
    if request.method == "GET":
        form.name.data = tag.name

    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag_count == 1 and Tag.name != data.get("name"):
            flash("标签已经存在，请重新输入!", "err")
            return redirect(url_for("admin.tag_edit", id=id))

        tag.name = data.get("name")

        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功！ ", 'info')
        return redirect(url_for("admin.tag_add", id=tag.id))

    return render_template("admin/tag_edit.html", form=form, tag=tag)

# 后端标签删除
@admin.route("/tag/del/<int:id>/", methods=["GET"])
@admin_login_req
def tag_del(id=None):
    movie = Tag.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash("删除标签成功！ ", 'OK')
    return redirect(url_for("admin.tag_list", page=1))

# 后端添加电影
@admin.route("/movie/add/", methods=["GET", "POST"])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        # 文件处理
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
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
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功！ ", 'info')
        return redirect(url_for("admin.movie_add"))

    return render_template("admin/movie_add.html", form=form)

# 后端电影列表
@admin.route("/movie/list/<int:page>/", methods=["GET"])
@admin_login_req
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)


# 后端编辑电影
@admin.route("/movie/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    form.url.flags.required = False
    form.logo.flags.required = False
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))
    # 如果是请求的话填充信息
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star

    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data["title"]).count()
        if movie_count == 1 and movie.title != data.get("title"):
            flash("片名已经存在，请重新输入!", "err")
            return redirect(url_for("admin.movie_edit", id=id))

        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")

        if form.url.data.filename != "":
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)

        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + movie.logo)

        movie.title = data.get("title")
        movie.info = data.get("info")
        movie.star = data.get("star")
        movie.tag_id = data.get("tag_id")
        movie.area = data.get("area")
        movie.release_time = data.get("release_time")
        movie.length = data.get("length")

        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功！ ", 'info')
        return redirect(url_for("admin.movie_add", id=movie.id))

    return render_template("admin/movie_edit.html", form=form, movie=movie)


# 后端删除电影
@admin.route("/movie/del/<int:id>/", methods=["GET"])
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash("删除电影成功！ ", 'OK')
    return redirect(url_for("admin.movie_list", page=1))

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