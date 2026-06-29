from flask import flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from MyFinance.utils.pg_utils import get_pg_utils

class AuthUtils:
    """Utility class containing class methods for auth routes."""

    @classmethod
    def register(cls):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            pg_utils = get_pg_utils()

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
            current_app.logger.warning(f'Error in register: {error}')
            flash(error)
        
        return render_template('auth/register.html',
            title='Regiser User',
            description='Enter the necessary user information'
        )

    @classmethod
    def login(cls):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            pg_utils = get_pg_utils()
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
                current_app.logger.warning(f'Error in login: {error}')
                flash(error)
        
        return render_template('auth/login.html',
            title='Login',
            description='Enter credentials'
        )

    @classmethod
    def load_logged_in_user(cls):
        user_id = session.get('user_id')
        pg_utils = get_pg_utils()
        if user_id is None:
            g.user = None
        else:
            g.user = pg_utils.get_user_by_id(user_id)

    @classmethod
    def logout(cls):
        session.clear()
        return redirect(url_for('home'))
