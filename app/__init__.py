from flask import Flask
from flask_login import LoginManager
from functools import wraps
from flask import current_app, abort

login_manager = LoginManager()
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "dqzldqz$dlqz"
login_manager.init_app(app)
login_manager.login_view = 'route_signin'
app.id = -1


@login_manager.user_loader
def user_loader(user_id):
    if app.id != -1:
        return app.id
    return None


def login_only(f):
    @wraps(f)
    def wrapped(**kwargs):
        if app.id == -1:
            abort(404)

        return f(**kwargs)
    return wrapped


def not_login_only(f):
    @wraps(f)
    def wrapped(**kwargs):
        if app.id != -1:
            abort(404)

        return f(**kwargs)
    return wrapped
