from MyFinance.utils.pg_utils import PgUtils

#from MyFinance.models.vouchers import Voucher, VoucherDetail
from MyFinance.models.entities import (Register, RegisterCode)

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, current_app
)
#from werkzeug.security import check_password_hash, generate_password_hash

from MyFinance.auth import login_required

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/')
@login_required
def enter_register():
    """route /register -- create a register entry
    
    Returns:
        renders register_entry.html and which post back to /register_result
    """
    
    pg_utils = PgUtils(current_app.config['PGURI'])
    return render_template(
        'register/register_entry.html',
        title='Register Entry',
        description = 'Create a register entry',
        code_list = pg_utils.get_codes(),
        account_list=pg_utils.get_external_accounts()    
    )
    
@bp.route('/register_result', methods=['POST', 'GET'])
def register_result():
    
    if request.method == 'POST':
        result = request.form
        #print(result)
        register = Register(external_account_id=result["pmt_account"],
                            code=result["code"],
                            date=result["date"],
                            description=result["description"],
                            debit=float(result["debit"]),
                            isFee=False,
                            credit=float(result["credit"]),
                            tran_no=int(result["tran_no"]))
        
        
        return render_template(
            'register/register_display.html',
            title = 'Register Display',
            description = 'Dispplays a register entry',
            register = register
        )