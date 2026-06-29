from flask import current_app, render_template, request
from MyFinance.utils.pg_utils import get_pg_utils
from MyFinance.models.payables import Liabilities

class LiabilityUtils:
    """Utility class containing class methods for each liability route."""

    @classmethod
    def enter_liability(cls):
        pg_utils = get_pg_utils()
        return render_template(
            'liability/liability_entry.html',
            title='Liability',
            description='Enter liability information',
            mode='enter',
            account_list=pg_utils.get_external_accounts()
        )

    @classmethod
    def liability_result(cls):
        if request.method == 'POST':
            results = request.form
            pg_utils = get_pg_utils() 
            new_id = pg_utils.get_next_liability_id()

            if results['payment_voucher_id'] == '':
                pmt_voucher_id = None
            else:
                pmt_voucher_id = int(results['payment_voucher_id'])   

            liability = Liabilities( 
                id=new_id,
                payment_voucher_id=pmt_voucher_id,
                external_account_id=results['external_account_id'],
                current_balance_dt=results['current_balance_dt'],
                current_balance_amt=results['current_balance_amt'],
                pmt_due_dt=results['pmt_due_dt'],
                pmt_due_amt=results['pmt_due_amt'],
                period_int=results['period_int']
            )

            pg_utils.add_liability(liability)
            liability_dict = pg_utils.get_liability(int(new_id))
            return render_template(
                'liability/liability_display.html',
                title='Liability',
                description='Display a liability',
                liability=liability_dict            
            )

    @classmethod
    def get_liability(cls, liability_id):
        pg_utils = get_pg_utils()
        liability_dict = pg_utils.get_liability(liability_id)
        if len(liability_dict) > 0:
            return render_template(
                'liability/liability_display.html',
                title='Liability',
                description='Display a liability',
                liability=liability_dict
            )
        else:
            current_app.logger.warning(f'In liability.get_liabiity: no data return for liability_id: {liability_id}')
            return render_template(
                'not_found.html',
                description=f'The liability {liability_id} was not found',
                title='No Such Liablity'
            )        

    @classmethod
    def get_liabiity_list(cls, account_number):
        pg_utils = get_pg_utils()
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
                description=f'The account {account_number} was not found',
                title='No Such Liablity'
            )
