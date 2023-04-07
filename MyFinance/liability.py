from MyFinance.utils.pg_utils import PgUtils

from MyFinance.models.payables import AccountsPayable

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, current_app
)
#from werkzeug.security import check_password_hash, generate_password_hash

from MyFinance.auth import login_required

bp = Blueprint('liability', __name__, url_prefix='/liability')

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
