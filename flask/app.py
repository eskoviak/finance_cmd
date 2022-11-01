import sys

sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
from crypt import methods

import pg_utils
from flask import Flask, render_template, request

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
    return render_template(
        'voucher_entry.html',
        title='Voucher Entry',
        description='Enter voucher data',
        vendor_list=pg_utils.get_vendors(),
        account_list = pg_utils.get_external_accounts()
    )


@app.route("/voucher_result", methods=['POST', 'GET'])
def voucher_result():

    if request.method == 'POST':
        result = request.form
    return render_template(
        'voucher_result.html',
        title="Voucher Entry Confirmation",
        description="You entered the following data:",
        result=result
    )
