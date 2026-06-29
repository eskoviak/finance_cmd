from flask import render_template, request
from MyFinance.utils.pg_utils import get_pg_utils
from MyFinance.models.entities import Register

class RegisterUtils:
    """Utility class containing class methods for each register route."""

    @classmethod
    def enter_register(cls):
        pg_utils = get_pg_utils()
        return render_template(
            'register/register_entry.html',
            title='Register Entry',
            description='Create a register entry',
            code_list=pg_utils.get_codes(),
            account_list=pg_utils.get_external_accounts()    
        )
        
    @classmethod
    def register_result(cls):
        if request.method == 'POST':
            result = request.form
            register = Register(
                external_account_id=result["pmt_account"],
                code=result["code"],
                date=result["date"],
                description=result["description"],
                debit=float(result["debit"]),
                isFee=False,
                credit=float(result["credit"]),
                tran_no=int(result["tran_no"])
            )
            
            return render_template(
                'register/register_display.html',
                title='Register Display',
                description='Dispplays a register entry',
                register=register
            )
