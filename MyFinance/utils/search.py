import inspect
from flask import render_template, request, current_app
from MyFinance.utils.pg_utils import get_pg_utils

class SearchUtils:
    """Utility class containing class methods for each search route."""

    @classmethod
    def search_objects(cls):
        __module__ = f'{inspect.stack()[0][0].f_code.co_name}'
        if request.method == 'POST':
            search_phrase = request.form["search_phrase"]
            voucher_list = []
            payable_list = []
            vendor_list = []
            pg_utils = get_pg_utils()
            try:
                if search_phrase.isdigit():
                    current_app.logger.info(f'{__module__} Search Phrase: {search_phrase}')
                    voucher_list.append(pg_utils.get_voucher(int(search_phrase)))
                    payable_list.append(pg_utils.get_payable(int(search_phrase)))
                else:
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
