from MyFinance.utils.pg_utils import PgUtils

#from MyFinance.models.vouchers import Voucher, VoucherDetail

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
                    return payable_dict
            else:
                current_app.logger.warning(f'In payable.get_payable: no data return for payable_id: {payable_id}')
                return render_template(
                        'not_found.html',
                        description='The payable {payable_id} as not found',
                        title='No such payable'
                )