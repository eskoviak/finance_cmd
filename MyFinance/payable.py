from MyFinance.utils.pg_utils import PgUtils

from MyFinance.models.payables import AccountsPayable

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, current_app
)
#from werkzeug.security import check_password_hash, generate_password_hash

from MyFinance.auth import login_required

bp = Blueprint('payable', __name__, url_prefix='/payable')

@bp.route('<int:payable_id>', methods=['GET']) #type: ignore
def get_payable(payable_id):
            pg_utils = PgUtils(current_app.config['PGURI'])
            payable_dict = pg_utils.get_payable(payable_id)
            if len(payable_dict) > 0:
                    return render_template(
                        'payable/payable_display.html',
                        title='Payable',
                        description='Display a payable',
                        payable=payable_dict
                    )
            else:
                current_app.logger.warning(f'In payable.get_payable: no data return for payable_id: {payable_id}')
                return render_template(
                        'not_found.html',
                        description='The payable {payable_id} was not found',
                        title='No Such payable'
                )
            
@bp.route('/') #type: ignore
def enter_payable():
        """/payable enter a payable

        Enter the data for a payable

        """
        pg_utils = PgUtils(current_app.config['PGURI'])
        return render_template(
                'payable/payable_entry.html',
                title='Payable Entry',
                description='Enter a payable',
                vendor_list=pg_utils.get_vendors(),
                account_list=pg_utils.get_external_accounts(),
                mode='enter'
                #voucher_type_list=pg_utils.get_voucher_types()
                #payment_type_list=pg_utils.get_payment_types()
        )

@bp.route('/edit/<int:payable_id>', methods=['POST', 'GET']) #type: ignore
def edit_payable(payable_id):
        return f'Coming soon, {payable_id}'

@bp.route('payable_result', methods=['POST', 'GET']) #type: ignore
def payable_result():
        """/payable/payable_result

        Target of the form on payable_entry.html
        """
        if request.method == 'POST':
                result = request.form
                ## Need to guard against empty string in int field
                if result['payment_voucher_id'] == '':
                        pmt_voucher_id = None
                else:
                        pmt_voucher_id = int(result['payment_voucher_id'])
                payable = AccountsPayable(
                        vendor_number=result['vendor'],
                        invoice_id = result['invoice_id'],
                        stmt_dt=result['stmt_dt'],
                        stmt_amt=result['stmt_amt'],
                        payment_due_dt=result['payment_due_dt'],
                        payment_source_id=result['payment_source'],
                        payment_voucher_id=pmt_voucher_id)
                pg_utils = PgUtils(current_app.config['PGURI'])
                ret_payable = pg_utils.add_payable(payable)
                payable = pg_utils.get_payable(ret_payable)
                return render_template(
                        'payable/payable_display.html',
                        title='Payable',
                        description='Display a payable',
                        payable=payable
                )
                           
                