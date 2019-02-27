# codeing:utf8
"""
flask web 例子
"""
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1 style='color:red'>hello lishan</h1>"


if __name__ == '__main__':
    app.run()