import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')

from flask import Flask, render_template, request, redirect, url_for
#from archive.models_tst import Voucher, VoucherDetail
from MyFinance.utils.pg_utils import PgUtils


# The application factory
def create_app(test_config=None):
    """
    Creates an Application Factory for the python (WSGI or Flask) application,

    :param test_config: Optional dictionary of configuration parmeters to be used.  If this value is not passed in, then the function looks in a
        top level folder ``instancd`` for a file named ``config.py``.  In either case, the values in will be stored in ``flask.current_app.config`` and may
        accessed from any child (configured blueprint).
    :type test_config: dict
    :return: app
    :rtype: Flask app object

    """
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

    # The Home page
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template(
            'home.html',
            title='Home',
            description='The MyFinance application home page'
        )

    @app.route('/help')
    def help():
        return render_template(
            'help/index.html'
        )
    
    @app.route('/login')
    def login():
        return redirect(url_for('auth.login'))
    
    from . import voucher
    app.register_blueprint(voucher.bp, )

    from . import auth
    app.register_blueprint(auth.bp)

    from . import payable
    app.register_blueprint(payable.bp)

    from . import liability
    app.register_blueprint(liability.bp)

    from . import search
    app.register_blueprint(search.bp)

    return app