from . import admin

@admin.route("/")
def index():
    return "<h1 style='color:green'>admin</h1>"