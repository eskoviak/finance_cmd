import functools
import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
from pg_utils import PgUtils

from models_tst import User

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pg_utils = PgUtils(current_app.config['PGURI'])

        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            userid = pg_utils.add_user(username, generate_password_hash(password))
            if userid == -1:
                error = 'User exists'
            else:        
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html',
        title='Regiser User',
        description='Enter the necessary user information'
    )

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pg_utils = PgUtils(current_app.config['PGURI'])
        user = pg_utils.get_user_by_name(username)
        error = None
        if len(user.keys()) == 0:
            error = "Username not found"
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password"
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            flash(error)
    return render_template('auth/login.html',
        title='Login',
        description='Enter credentials')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    pg_utils = PgUtils(current_app.config['PGURI'])
    if user_id == None:
        g.user = None
    else:
        g.user = pg_utils.get_user_by_id(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view