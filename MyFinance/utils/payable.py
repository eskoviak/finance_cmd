import inspect
from flask import render_template, request, current_app
from MyFinance.utils.pg_utils import get_pg_utils
from MyFinance.models.payables import AccountsPayable

class PayableUtils:
    """Utility class containing class methods for each payable route."""

    @classmethod
    def get_payable(cls, payable_id):
        pg_utils = get_pg_utils()
        payable_dict = pg_utils.get_payable(payable_id)
        if len(payable_dict) > 0:
            return render_template(
                'payable/payable_display.html',
                title='Payable',
                description='Display a payable',
                payable=payable_dict                        
            )
        else:
            current_app.logger.warning(f'{inspect.stack()[0][0].f_code.co_name}: no data return for payable_id: {payable_id}')
            return render_template(
                'not_found.html',
                description=f'The payable {payable_id} was not found',
                title='No Such payable'
            )

    @classmethod
    def enter_payable(cls):
        pg_utils = get_pg_utils()
        return render_template(
            'payable/payable_entry.html',
            title='Payable Entry',
            description='Enter a payable',
            vendor_list=pg_utils.get_vendors(),
            account_list=pg_utils.get_external_accounts(),
            mode='enter'
        )

    @classmethod
    def edit_payable(cls, payable_id):
        pg_utils = get_pg_utils()
        if request.method == 'GET':
            payable_dict = pg_utils.get_payable(payable_id)
            if len(payable_dict) > 0:
                return render_template(
                    'payable/payable_edit.html',
                    title='Edit Payable',
                    description='Edit a payable',
                    payable=payable_dict,
                    account_list=pg_utils.get_external_accounts()
                )
            else:
                current_app.logger.warning(f'edit_payable: no data for payable_id: {payable_id}')
                return render_template(
                    'not_found.html',
                    description=f'The payable {payable_id} was not found',
                    title='No Such Payable'
                )
        else:
            result = request.form
            payment_voucher_id = int(result['payment_voucher_id']) if result.get('payment_voucher_id') else None
            pg_utils.update_payable(
                payable_id=payable_id,
                stmt_amt=float(result['stmt_amt']),
                payment_due_dt=result['payment_due_dt'],
                payment_source_id=int(result['payment_source_id']),
                payment_voucher_id=payment_voucher_id,
                invoice_id=result['invoice_id']
            )
            return cls.get_payable(payable_id)

    @classmethod
    def get_open_payables(cls):
        pg_utils = get_pg_utils()
        return render_template(
            'payable/payable_list.html',
            title='Open Payables',
            description='Unpaid payables due within the next 20 days',
            payable_list=pg_utils.get_open_payables()
        )

    @classmethod
    def get_payable_by_vendor(cls, vendor_number: int):
        pg_utils = get_pg_utils()
        return render_template(
            'payable/payable_list.html',
            title='Payables',
            description=f'List of payables by Vendor_number {vendor_number}',
            payable_list=pg_utils.get_payable_by_vendor(vendor_number)
        )

    @classmethod
    def payable_result(cls):
        if request.method == 'POST':
            result = request.form
            # Need to guard against empty string in int field
            if result['payment_voucher_id'] == '':
                pmt_voucher_id = None
            else:
                pmt_voucher_id = int(result['payment_voucher_id'])
                
            if result.get('vendor_account') == '' or result.get('vendor_account') is None:
                vendor_acct = None
            else:
                vendor_acct = int(result['vendor_account'])
                
            payable = AccountsPayable(
                vendor_number=result['vendor'],
                invoice_id=result['invoice_id'],
                stmt_dt=result['stmt_dt'],
                stmt_amt=result['stmt_amt'],
                payment_due_dt=result['payment_due_dt'],
                payment_source_id=result['payment_source'],
                payment_voucher_id=pmt_voucher_id,
                vendor_account=vendor_acct
            )
            pg_utils = get_pg_utils()
            ret_payable = pg_utils.add_payable(payable)
            payable_dict = pg_utils.get_payable(ret_payable)
            return render_template(
                'payable/payable_display.html',
                title='Payable',
                description='Display a payable',
                payable=payable_dict
            )
