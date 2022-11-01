import sys

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
from models_tst import (Voucher, Vendors, ExternalAccounts, VoucherType, PaymentType)

pg_uri = "postgresql://postgres:terces##@localhost:5432/finance"

def get_voucher(voucher_number : int) -> dict:
    """gets the voucher and vourcher details in JSON format for the given voucher_number

    Args:
        voucher_number (int): The voucher number

    Returns:
        A dict object
    """
    engine = create_engine(pg_uri)
    with Session(engine) as session:
        results = session.execute(select(Voucher).where(Voucher.voucher_number == voucher_number))
        voucher_dict = {}
        voucher_detail = []
        for row in results:
            #print(row.Voucher.voucher_number)
            voucher_dict["voucher_number"] = row.Voucher.voucher_number
            voucher_dict["voucher_date"] = row.Voucher.voucher_date.isoformat()
            voucher_dict["voucher_ref"] = row.Voucher.voucher_ref
            voucher_dict["voucher_amt"] = row.Voucher.voucher_amt
            voucher_dict["voucher_type"] = row.Voucher.voucher_type.type_text
            voucher_dict["vendor"] = row.Voucher.vendor.vendor_short_desc
            voucher_dict["payment_type"] = row.Voucher.payment_type.payment_type_text
            voucher_dict["payment_source"] = row.Voucher.payment_source.account_name
            voucher_dict["payment_ref"] = row.Voucher.payment_ref
            for detail in row.Voucher.details:
                voucher_line = {}
                voucher_line["split_seq_number"] = detail.split_seq_number
                voucher_line["account_number"] = detail.account_number
                voucher_line["amount"] = detail.amount
                voucher_line["dimension_1"] = detail.dimension_1
                voucher_line["dimension_2"] = detail.dimension_2
                voucher_line["memo"] = detail.memo
                voucher_detail.append(voucher_line)
            voucher_dict["Splits"] = voucher_detail

    return voucher_dict

def get_vendors() -> list:
    """gets the list of vendors

    Returns:
        dict: [{vendor_short_desc: vendor_number}, ...]
    """
    engine = create_engine(pg_uri)
    with Session(engine) as session:
        results = session.query(Vendors).order_by(Vendors.vendor_short_desc)
        vendor_list = []
        for row in results:
            vendor = {}
            vendor["vendor_short_desc"] = row.vendor_short_desc
            vendor["vendor_number"] = row.vendor_number
            vendor_list.append(vendor)

        return vendor_list

def get_external_accounts() -> list:
    """gets the list of external accounts

    Returns:
        disc: [{account_name: external_account_id}]
    """
    with Session(create_engine(pg_uri)) as session:
        results = session.query(ExternalAccounts).order_by(ExternalAccounts.account_name)
        account_list = []
        for row in results:
            account = {}
            account["account_name"] = row.account_name
            account["external_account_id"] = row.external_account_id
            account_list.append(account)

        return account_list