from MyFinance.utils.register import RegisterUtils
from flask import Blueprint
from MyFinance.auth import login_required

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/')
@login_required
def enter_register():
    """route /register -- create a register entry
    
    Returns:
        renders register_entry.html and which post back to /register_result
    """
    return RegisterUtils.enter_register()
    
@bp.route('/register_result', methods=['POST', 'GET'])
def register_result():
    return RegisterUtils.register_result()