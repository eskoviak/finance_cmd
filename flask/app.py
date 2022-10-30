import sys

#from django.shortcuts import render

sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
#import json

import pg_utils
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        'home.html',
        title='Finance Site',
        description = 'The main finance site'
    )
    

@app.route("/voucher/<int:voucher_number>")
def get_voucher(voucher_number):
    voucher_dict = pg_utils.get_voucher(voucher_number)
    if len(voucher_dict) > 0:
        return render_template(
            'voucher_display.html',
            title='Voucher Display',
            description = '===',
            data = voucher_dict
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
        #)
    else:
        return "Not Found"