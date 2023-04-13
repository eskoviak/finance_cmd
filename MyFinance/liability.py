from MyFinance.utils.pg_utils import PgUtils

from MyFinance.models.payables import AccountsPayable,Liabilities

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, current_app
)
#from werkzeug.security import check_password_hash, generate_password_hash

from MyFinance.auth import login_required

bp = Blueprint('liability', __name__, url_prefix='/liability')

@bp.route('/', methods=['GET']) #type: ignore
def enter_liability():
    pg_utils = PgUtils(current_app.config['PGURI'])
    
    return render_template(
        'liability/liability_entry.html',
        title='Liability',
        description = 'Enter liability information',
        mode='enter',
        account_list=pg_utils.get_external_accounts()
    )

@bp.route('liability_result', methods=['GET', 'POST']) #type: ignore
def liability_result():
    if request.method == 'POST':
        results = request.form
        pg_utils = PgUtils(current_app.config['PGURI']) 
        new_id = pg_utils.get_next_liability_id()

        ## Need to guard against empty string in int field
        if results['payment_voucher_id'] == '':
            pmt_voucher_id = None
        else:
            pmt_voucher_id = int(results['payment_voucher_id'])   

        liability = Liabilities( 
            id = new_id,
            payment_voucher_id = pmt_voucher_id,
            external_account_id = results['external_account_id'],
            current_balance_dt = results['current_balance_dt'],
            current_balance_amt = results['current_balance_amt'],
            pmt_due_dt = results['pmt_due_dt'],
            pmt_due_amt = results['pmt_due_amt'],
            period_int = results['period_int']
        )

        pg_utils.add_liability(liability)
        liability_dict = pg_utils.get_liability(int(new_id)) #type: ignore
        return render_template(
            'liability/liability_display.html',
            title='Liability',
            description = 'Display a liability',
            liability=liability_dict            

        )

        return results

@bp.route('<int:liability_id>', methods=['GET']) #type: ignore
def get_liability(liability_id):
    pg_utils = PgUtils(current_app.config['PGURI'])
    liability_dict = pg_utils.get_liability(liability_id)
    if len(liability_dict) > 0:
        return render_template(
            'liability/liability_display.html',
            title='Liability',
            description = 'Display a liability',
            liability=liability_dict
        )
    else:
        current_app.logger.warning(f'In liability.get_liabiity: no data return for liability_id: {payable_id}')
        return render_template(
                'not_found.html',
                description='The liability {liability_id} was not found',
                title='No Such Liablity'
        )        

@bp.route('/liability/<int:account_number>', methods=['GET']) #type: ignore
def get_liabiity_list(account_number):
    pg_utils = PgUtils(current_app.config['PGURI'])
    liability_list = pg_utils.get_liability_by_account(account_number)
    if len(liability_list) > 0:
        return render_template(
            'liability/liability_list.html',
            title='List Liabilities',
            description=f"Current liabilities for {account_number}",
            liability_list=liability_list
        )
    else:
        current_app.logger.warning(f'In liability.get_liabiity_list: no data return for account_number: {account_number}')
        return render_template(
                'not_found.html',
                description='The account {account_number} was not found',
                title='No Such Liablity'
        )          

    