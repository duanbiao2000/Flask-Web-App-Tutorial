from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # 从当前目录下的views模块中导入views
    from .views import views
    # 从当前目录下的auth模块中导入auth
    from .auth import auth

    # 注册视图蓝图，设置URL前缀为'/'
    app.register_blueprint(views, url_prefix='/')
    # 注册认证蓝图，设置URL前缀为'/'
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    # 创建一个LoginManager对象
    login_manager = LoginManager()
    # 设置登录视图为auth.login
    login_manager.login_view = 'auth.login'
    # 初始化app
    login_manager.init_app(app)

    """ @login_manager.user_loader 是 Flask-Login 扩展中的一个装饰器，
    用于加载用户对象。
    Flask-Login 是一个用于管理用户会话的 Flask 扩展，它允许你轻松地处理用户登录、登出和会话管理。 """
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
