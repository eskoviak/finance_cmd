from MyFinance.utils.pg_utils import PgUtils

from MyFinance.models.payables import AccountsPayable

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, current_app
)
#from werkzeug.security import check_password_hash, generate_password_hash

from MyFinance.auth import login_required

import inspect

bp = Blueprint('search', __name__, url_prefix='/search')
@bp.route('/', methods=['POST']) #type: ignore
def search_objects():
    __module__ = f'{inspect.stack()[0][0].f_code.co_name}'
    if request.method == 'POST':
        search_phrase = request.form["search_phrase"]
        voucher_list = []
        payable_list = []
        vendor_list = []
        ## is the search phrase a number? Must be an id
        pg_utils = PgUtils(current_app.config['PGURI'])
        try:
            if search_phrase.isdigit():
                current_app.logger.info(f'{__module__} Search Phrase: {search_phrase}')
                ## Voucher
                voucher_list.append(pg_utils.get_voucher(int(search_phrase)))
                ## Payable
                payable_list.append(pg_utils.get_payable(int(search_phrase)))
            else:
                ## Vendor
                current_app.logger.info(f'{__module__} Search Phrase: {search_phrase}')
                vendor_list = pg_utils.get_vendors(filter=str(search_phrase))
                current_app.logger.info(f'DB call returned {len(vendor_list)}')
            return render_template(
                'search/global_search.html',
                title='Global Search',
                description='Global Search Results',
                vouchers=voucher_list,
                vendors=vendor_list,
                payables=payable_list
            )
            
        except Exception as ex:
            current_app.logger.error(f"{__module__}: { ex.args[0]}")
            return render_template(
                'home.html'
            )
    
    

