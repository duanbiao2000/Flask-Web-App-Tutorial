from . import db
# 导入Flask-Login中的UserMixin类
""" UserMixin类提供了以下属性和方法：
is_authenticated：一个布尔属性，表示用户是否已经通过身份验证。
is_active：一个布尔属性，表示用户是否处于活动状态（例如，账户是否被禁用）。
is_anonymous：一个布尔属性，表示用户是否是匿名用户。
get_id()：一个方法，返回用户的唯一标识符，通常是一个字符串或数字。 """
from flask_login import UserMixin
# 导入SQLAlchemy的func模块，用于执行SQL函数
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# (db.Model, UserMixin): 这个类继承了 db.Model 和 UserMixin。
# 这意味着 User 类不仅是一个数据库模型，还拥有用户认证的一些常用方法。


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
