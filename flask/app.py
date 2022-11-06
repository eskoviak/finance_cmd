import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')

from flask import Flask, render_template, request
from models_tst import Voucher, VoucherDetail
from pg_utils import PgUtils




#import json


app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        'home.html',
        title='Finance Site',
        description='The main finance site'
    )


@app.route("/voucher/<int:voucher_number>", methods=['GET'] ) # type: ignore
def get_voucher(voucher_number):
    pg_utils = PgUtils()
    voucher_dict = pg_utils.get_voucher(voucher_number)
    if request.method == 'GET':
        if len(voucher_dict) > 0:
            return render_template(
                'voucher_display.html',
                title='Voucher Display',
                description='Displays voucher data for the selected vouher',
                data=voucher_dict
            )
        else:
            # TODO make pretty
            return "Not Found"




@app.route("/voucher")
def enter_voucher():
    """route /voucher -- create a voucher entry

    Returns:
        renders voucher_entry.html 
    """
    pg_utils = PgUtils()
    return render_template(
        'voucher_entry.html',
        title='Voucher Entry',
        description='Enter voucher data',
        vendor_list=pg_utils.get_vendors(),
        account_list=pg_utils.get_external_accounts(),
        voucher_type_list=pg_utils.get_voucher_types(),
        payment_type_list=pg_utils.get_payment_types()
    )


@app.route("/voucher_result", methods=['POST', 'GET'])  # type: ignore
def voucher_result():

    if request.method == 'POST':
        result = request.form
        voucher = Voucher(voucher_date=result["voucher_date"],
                          voucher_ref=result["voucher_ref"],
                          vendor_number=result["vendor"],
                          voucher_type_id=result["voucher_type"],
                          voucher_amt=result["voucher_amt"],
                          payment_type_id=result["payment_type"],
                          payment_source_id=result["pmt_account"],
                          payment_ref=result["payment_ref"])
        pg_utils = PgUtils()
        ret_voucher = pg_utils.add_voucher(voucher)
        voucher = pg_utils.get_voucher(int(ret_voucher))  # type: ignore
        # get_voucher(ret_voucher)
        # return render_template(
        #    'voucher_result.html',
        #    title="Voucher Entry Confirmation",
        #    description="You entered the following data:",
        #    result=result,
        #    voucher_data=ret_voucher
        # )
        return render_template(
            'voucher_display.html',
            title='Voucher Display',
            description='Displays voucher data for the selected vouher',
            data=voucher
        )


# type: ignore
@app.route("/detail_entry", methods=['POST'])
@app.route("/detail_entry/<int:voucher_number>/<int:split_seq_number>", methods=['GET']) # type: ignore
def detail_entry(voucher_number=None, split_seq_number=None):
    pg_utils = PgUtils()
    if request.method == 'POST':
        result = request.form
        voucher_number = result['voucher_number'] # type: ignore
        split_seq_number = pg_utils.get_next_split_number(int(voucher_number))
        #return f"In detail_entry =={voucher_number}:{split_seq_num}==" #type: ignore
    return render_template(
        "detail_entry.html",
        title="Voucher Detail Entry",
        description="Enter the voucher detail line items",
        voucher_number=voucher_number,
        split_seq_number=split_seq_number
    )

@app.route("/detail_result", methods = ['POST']) # type: ignore
def detail_result():
    if request.method == 'POST':
        result = request.form
        voucher_detail = VoucherDetail(
            voucher_number = result["voucher_number"],
            split_seq_number = result["split_seq_number"],
            account_number = result["account_number"],
            amount = result["amount"],
            dimension_1 = result["dimension_1"],
            dimension_2 = result["dimension_2"],
            memo = result["memo"]
        )
        pg_utils = PgUtils()
        ret_seq = pg_utils.add_voucher_details(voucher_detail)
        voucher = pg_utils.get_voucher(int(voucher_detail.voucher_number))
        return render_template(
            'voucher_display.html',
            title='Voucher Display',
            description='Displays voucher data for the selected vouher',
            data=voucher
        )            


        



