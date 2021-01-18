from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import jsonify
from hashlib import md5
from app import db, login


@login.user_loader  # 引用current_user时，Flask-Login将调用用户加载函数
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)  # index为True表示可索引
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # backref参数：为用户动态添加了author属性
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # 该方法打印实例对象是自动调用
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # print(password.data)  # 注意这里的password为一个密码类型的对象，需要通过其data属性得到其值
        return check_password_hash(self.password_hash, password.data)  # 若直接传password会报错 TypeError: Expected bytes

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 本处的user是数据库表的名称，Flask-SQLAlchemy自动设置类名为小写来作为对应表的名称

    def __repr__(self):
        return '<Post {}>'.format(self.body)
