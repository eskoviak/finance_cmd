import functools
from flask import Blueprint, g, redirect, url_for
from MyFinance.utils.auth import AuthUtils

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    return AuthUtils.register()

@bp.route('/login', methods=('GET', 'POST'))
def login():
    return AuthUtils.login()

@bp.before_app_request
def load_logged_in_user():
    return AuthUtils.load_logged_in_user()

@bp.route('/logout')
def logout():
    return AuthUtils.logout()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view