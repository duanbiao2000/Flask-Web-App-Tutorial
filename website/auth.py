from flask import Blueprint, render_template, request, flash, redirect, url_for

"""
 1. **`from flask import Blueprint`**:
 - 这行代码从Flask库中导入`Blueprint`类。`Blueprint`是Flask中用于组织应用模块的一种方式。通过使用蓝图，可以将应用的不同部分（如用户认证、博客文章、API端点等）分离成独立的模块，从而提高代码的可维护性和可扩展性。

2. **`render_template`**:
   - `render_template`是一个Flask函数，用于渲染HTML模板。它接受一个模板文件名作为参数，并返回渲染后的HTML内容。模板文件通常位于`templates`文件夹中，使用Jinja2模板引擎来处理动态内容。

3. **`request`**:
   - `request`是一个全局对象，用于访问客户端发送的HTTP请求信息。它包含了请求的URL、表单数据、文件上传等。通过`request`对象，可以获取客户端发送的数据，并进行相应的处理。

4. **`flash`**:
   - `flash`是一个Flask函数，用于在请求之间传递消息。它通常用于在用户执行某个操作后，向用户显示一条消息（如成功或错误信息）。`flash`函数会将消息存储在会话中，以便在下一个请求中通过`get_flashed_messages`函数获取。

5. **`redirect`**:
   - `redirect`是一个Flask函数，用于重定向用户到另一个URL。它接受一个URL作为参数，并返回一个重定向响应。重定向通常用于在用户执行某个操作后，将用户引导到不同的页面。

6. **`url_for`**:
   - `url_for`是一个Flask函数，用于生成URL。它接受视图函数的名称作为参数，并返回该视图函数对应的URL。这对于在模板中生成链接非常有用，可以确保链接始终指向正确的URL，即使URL发生变化。

**用途**：
这段代码主要用于设置Flask应用的路由和视图函数。通过导入这些函数，可以创建蓝图、渲染模板、处理请求、显示消息、重定向用户以及生成URL。

**注意事项**：
- 确保在Flask应用中正确配置了模板文件夹（通常是`templates`）。
- 使用`flash`函数时，需要在应用中启用会话（通过`app.secret_key`设置一个密钥）。
- 在使用`url_for`生成URL时，确保视图函数已经注册到应用的路由中。  """
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


""" 这段代码是从Flask-Login库中导入了一些函数和类，用于处理用户登录、登出和当前用户相关的操作。Flask-Login是一个用于Flask框架的扩展，它简化了用户会话管理，使得开发者可以更容易地实现用户认证功能。

具体来说，这段代码导入了以下内容：

1. `login_user(user, remember=False)`：这个函数用于登录用户。它接受一个用户对象作为参数，并将其与当前会话关联起来。`remember`参数是一个布尔值，用于指定是否在客户端上记住用户（通常通过设置cookie来实现）。

2. `login_required`：这是一个装饰器，用于保护视图函数，使其只能被已登录的用户访问。如果未登录的用户尝试访问被装饰的视图函数，Flask-Login会自动重定向到登录页面。

3. `logout_user()`：这个函数用于登出当前用户。它会清除当前会话中的用户信息，从而结束用户的会话。

4. `current_user`：这是一个代理对象，用于访问当前登录的用户。它提供了一些属性和方法，如`is_authenticated`（检查用户是否已认证）、`is_active`（检查用户是否处于活动状态）和`id`（获取用户的唯一标识符）。

用途：
- 实现用户登录和登出功能。
- 保护需要认证的视图函数，确保只有已登录的用户才能访问。
- 获取当前登录的用户信息。

注意事项：
- 使用Flask-Login时，需要先创建一个用户模型，并实现Flask-Login所需的用户加载方法（如`get_user`）。
- 在使用`login_user`函数时，需要确保用户对象已经通过某种方式（如数据库查询）进行了初始化。
- `login_required`装饰器可以应用于视图函数，以限制访问权限。
- `current_user`对象可以在视图函数中用于获取当前登录的用户信息。 """
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

# 查询数据库中email字段等于传入参数email的第一个User对象
        user = User.query.filter_by(email=email).first()
        if user:
            # 检查密码是否匹配
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# 定义一个路由，路径为/sign-up，支持GET和POST请求
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # 如果请求方法为POST
    if request.method == 'POST':
        # 获取表单中的email、first_name、password1、password2
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 查询数据库中是否存在该email的用户
        user = User.query.filter_by(email=email).first()
        # 如果存在，则提示Email already exists.
        if user:
            flash('Email already exists.', category='error')
        # 如果email长度小于4，则提示Email must be greater than 3 characters.
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        # 如果first_name长度小于2，则提示First name must be greater than 1 character.
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        # 如果password1和password2不相等，则提示Passwords don't match.
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        # 如果password1长度小于7，则提示Password must be at least 7 characters.
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        # 否则，创建新用户，并添加到数据库中
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # 登录新用户
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # 重定向到主页
            return redirect(url_for('views.home'))

    # 返回注册页面，并传递当前用户信息
    return render_template("sign_up.html", user=current_user)
