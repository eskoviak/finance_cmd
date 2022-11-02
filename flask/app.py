import sys

sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')

from flask import Flask, render_template, request
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


@app.route("/voucher/<int:voucher_number>")
def get_voucher(voucher_number):
    pg_utils = PgUtils()
    voucher_dict = pg_utils.get_voucher(voucher_number)
    if len(voucher_dict) > 0:
        return render_template(
            'voucher_display.html',
            title='Voucher Display',
            description='Displays voucher data for the selected vouher',
            data=voucher_dict
        )
        #number = voucher_dict["voucher_number"],
        #date = voucher_dict["voucher_date"],
        #ref = voucher_dict["voucher_ref"],
        #amount = voucher_dict["voucher_amt"],
        #type = voucher_dict["voucher_type"],
        #vendor = voucher_dict["vendor"],
        #ptype = voucher_dict["payment_type"],
        #psource = voucher_dict["payment_source"],
        #pref = voucher_dict["payment_ref"],
        #splits = voucher_dict["Splits"]
        # )
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
        account_list = pg_utils.get_external_accounts(),
        voucher_type_list = pg_utils.get_voucher_types(),
        payment_type_list = pg_utils.get_payment_types()
    )


@app.route("/voucher_result", methods=['POST', 'GET']) # type: ignore
def voucher_result():

    if request.method == 'POST':
        result = request.form
        return render_template(
            'voucher_result.html',
            title="Voucher Entry Confirmation",
            description="You entered the following data:",
            result=result
        )
