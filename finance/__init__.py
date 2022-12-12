import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')

from flask import Flask, render_template, request, redirect, url_for
from models_tst import Voucher, VoucherDetail
from pg_utils import PgUtils


# The application factory
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # a simple page that says hello
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template(
            'home.html',
            title='Home',
            description='The Finance application home page'
        )

    @app.route('/login')
    def login():
        return redirect(url_for('auth.login'))
    
    from . import voucher
    app.register_blueprint(voucher.bp, )

    from . import auth
    app.register_blueprint(auth.bp)

    return app