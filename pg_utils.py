import sys

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
from dotenv import dotenv_values

from models_tst import (ExternalAccounts, PaymentType, Vendors, Voucher,
                        VoucherType, VoucherDetail)


class PgUtils:
    """This class encapsulates the various functions needed by the finance application

    """

    config = {}

    def __init__(self):
        self.config = dotenv_values(".env")
        #self.config["PGURI"] = "postgresql://postgres:terces##@localhost:5432/finance"

    def get_voucher(self, voucher_number : int) -> dict:
        """gets the voucher and vourcher details in JSON format for the given voucher_number

        Args:
            voucher_number (int): The voucher number

        Returns:
            A dict object
        """
        with Session(create_engine("postgresql://postgres:terces##@localhost:5432/finance")) as session:
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

    def get_vendors(self) -> list:
        """gets the list of vendors

        Returns:
            dict: [{vendor_short_desc: vendor_number}, ...]
        """
        vendor_list = []
        try:
            with Session(create_engine("postgresql://postgres:terces##@localhost:5432/finance")) as session: # type: ignore
                results = session.query(Vendors).order_by(Vendors.vendor_short_desc)
                for row in results:
                    vendor = {}
                    vendor["vendor_short_desc"] = row.vendor_short_desc
                    vendor["vendor_number"] = row.vendor_number
                    vendor_list.append(vendor)
        except (Exception):
            print(Exception.__name__)

        return vendor_list

    def get_external_accounts(self) -> list:
        """gets the list of external accounts

        Returns:
            disc: [{account_name: external_account_id}, ...]
        """
        account_list = []
        try:
            with Session(create_engine("postgresql://postgres:terces##@localhost:5432/finance")) as session:  # type: ignore
                results = session.query(ExternalAccounts).order_by(ExternalAccounts.account_name)

                for row in results:
                    account = {}
                    account["account_name"] = row.account_name
                    account["external_account_id"] = row.external_account_id
                    account_list.append(account)
        except (Exception):
            print(Exception.__name__)

        return account_list

    def get_voucher_types(self) -> list:
        """gets the list of voucher types

        Returns:
            list: [{type_text, type_code}, ...]
        """
        voucher_types = []
        try:
            with Session(create_engine("postgresql://postgres:terces##@localhost:5432/finance")) as session:  # type: ignore
                results = session.query(VoucherType).order_by(VoucherType.type_text)

                for row in results:
                    type = {}
                    type["type_text"] = row.type_text
                    type["type_code"] = row.type_code
                    voucher_types.append(type)
        except (Exception):
            print (Exception.__name__)

        return voucher_types

    def get_payment_types(self) -> list:
        """gets the list of payment types

        Returns:
            list: [{payment_type_text: payment_type_id}, ...]
        """
        payment_types = []
        try:
            with Session(create_engine("postgresql://postgres:terces##@localhost:5432/finance")) as session:  # type: ignore
                results = session.query(PaymentType).order_by(PaymentType.payment_type_text)

                for row in results:
                    pmt_type = {}
                    pmt_type['payment_type_text'] = row.payment_type_text
                    pmt_type['payment_type_id'] = row.payment_type_id
                    payment_types.append(pmt_type)
        except (Exception):
            print (Exception.__name__)

        return payment_types

    def add_voucher(self, Voucher):

        try:
            with Session(create_engine("postgresql://postgres:terces##@localhost:5432/finance")) as session: # type: ignore
                session.add(Voucher)
                session.commit()
                session.refresh(Voucher)
                return Voucher.voucher_number
        except (Exception):
            print (Exception.__name__)
            return Exception.__repr__

    def add_voucher_details(self, VoucherDetail):
        try:
            with Session(create_engine("postgresql://postgres:terces##@localhost:5432/finance")) as session: # type: ignore
                session.add(VoucherDetail)
                session.commit()
                session.refresh(VoucherDetail)
                return VoucherDetail.id
        except (Exception):
            return Exception.__repr__            

    def get_next_split_number(self, voucher_number : int):

        try:
            with Session(create_engine("postgresql://postgres:terces##@localhost:5432/finance")) as session: # type: ignore
                result = session.query(VoucherDetail.id).where(VoucherDetail.voucher_number == voucher_number)
                return len(result.all()) + 1 
                #return int(result.scalar()) + 1
        except (Exception):
            return Exception.__repr__
        