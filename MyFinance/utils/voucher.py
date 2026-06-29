from flask import current_app, flash, redirect, render_template, request, session
from MyFinance.utils.pg_utils import get_pg_utils
from MyFinance.models.vouchers import Voucher, VoucherDetail

class VoucherUtils:
    """Utility class containing class methods for voucher routes."""

    @classmethod
    def get_voucher(cls, voucher_number):
        if request.method == 'GET':
            pg_utils = get_pg_utils()
            voucher_dict = pg_utils.get_voucher(voucher_number)
            if len(voucher_dict) > 0:
                try:
                    session['voucher_amt'] = voucher_dict['voucher_amt']
                except KeyError:
                    session['voucher_amt'] = 0
                return render_template(
                    'voucher/voucher_display.html',
                    title='Voucher Display',
                    description='Displays voucher data for the selected vouher',
                    data=voucher_dict,
                    detail_total=pg_utils.get_detail_total(voucher_number)
                )
            else:
                current_app.logger.warning(f'In get_voucher: no data for voucher_number {voucher_number}')
                return render_template(
                    'not_found.html',
                    title='No Such Voucher',
                    description=f'The voucher {voucher_number} was not found'
                )

    @classmethod
    def enter_voucher(cls):
        pg_utils = get_pg_utils()
        session['voucher_amt'] = 0
        voucher_types = pg_utils.get_voucher_types()
        selected_voucher_type = None
        for voucher_type in voucher_types:
            type_text = str(voucher_type.get('type_text', '')).strip().lower()
            if 'paper' in type_text:
                selected_voucher_type = voucher_type.get('type_code')
                break

        return render_template(
            'voucher/voucher_entry.html',
            title='Voucher Entry',
            description='Enter voucher data',
            vendor_list=pg_utils.get_vendors(),
            account_list=pg_utils.get_external_accounts(),
            voucher_type_list=voucher_types,
            selected_voucher_type=selected_voucher_type,
            payment_type_list=pg_utils.get_payment_types(),
            company_list=pg_utils.get_company()
        )

    @classmethod
    def voucher_result(cls):
        if request.method == 'POST':
            result = request.form
            voucher = Voucher(
                voucher_date=result["voucher_date"],
                voucher_ref=result["voucher_ref"],
                vendor_number=result["vendor"],
                voucher_type_id=result["voucher_type"],
                voucher_amt=result["voucher_amt"],
                payment_type_id=result["payment_type"],
                payment_source_id=result["pmt_account"],
                payment_ref=result["payment_ref"],
                company_id=result["company"]
            )
                              
            pg_utils = get_pg_utils()
            ret_voucher = pg_utils.add_voucher(voucher)
            voucher_dict = pg_utils.get_voucher(int(ret_voucher))
            session['voucher_amt'] = voucher_dict.get('voucher_amt', 0)
            return render_template(
                'voucher/voucher_display.html',
                title='Voucher Display',
                description='Displays voucher data for the selected vouher',
                data=voucher_dict,
                detail_total=0
            )

    @classmethod
    def detail_entry(cls, voucher_number=None, split_seq_number=None):
        pg_utils = get_pg_utils()
        voucher_remain = 0
        if request.method == 'POST':
            result = request.form
            voucher_number = result['voucher_number']
            split_seq_number = pg_utils.get_next_split_number(int(voucher_number))
            voucher_remain = session.get('voucher_amt', 0)
            voucher_remain -= pg_utils.get_detail_total(int(voucher_number))
            
        return render_template(
            "voucher/detail_entry.html",
            title="Voucher Detail Entry",
            description="Enter the voucher detail line items",
            voucher_number=voucher_number,
            split_seq_number=split_seq_number,
            voucher_remain=round(voucher_remain, 2)
        )

    @classmethod
    def detail_result(cls):
        if request.method == 'POST':
            result = request.form
            voucher_detail = VoucherDetail(
                voucher_number=result["voucher_number"],
                split_seq_number=result["split_seq_number"],
                account_number=result["account_number"],
                amount=result["amount"],
                dimension_1=result["dimension_1"],
                dimension_2=result["dimension_2"],
                memo=result["memo"]
            )
            pg_utils = get_pg_utils()
            pg_utils.add_voucher_details(voucher_detail)
            voucher_dict = pg_utils.get_voucher(int(voucher_detail.voucher_number))
            return render_template(
                'voucher/voucher_display.html',
                title='Voucher Display',
                description='Displays voucher data for the selected vouher',
                data=voucher_dict,
                detail_total=pg_utils.get_detail_total(int(voucher_detail.voucher_number))
            )

    @classmethod
    def search(cls):
        if request.method == 'POST':
            search_phrase = request.form["search_phrase"]
            try:
                voucher_number = int(search_phrase)
                if voucher_number > 0:
                    return redirect(str(voucher_number))
                else:
                    flash('Voucher Number less than zero', 'error')
                    return render_template('home.html')
            except Exception as ex:
                current_app.logger.error(f"Exception in voucher.search: { ex.args[0]}")
                return render_template('home.html')
