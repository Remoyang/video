# codeing:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:123456@192.168.168.100:30006/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db=SQLAlchemy(app)


class User(db.Model):
    __tbalename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pwd = db.Column()
    email = db.Column()
    phone = db.Column()
    info = db.Column()
    face = db.Column()
    addtim = db.Column()



if __name__ == '__main__':
    app.run()