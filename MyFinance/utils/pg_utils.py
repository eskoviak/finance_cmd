from sqlalchemy import create_engine, select, text, func, Sequence
from sqlalchemy.orm import Session, sessionmaker

from MyFinance.models.user import User
from MyFinance.models.vendors import Vendors
from MyFinance.models.vouchers import (Voucher, VoucherDetail, VoucherType)
from MyFinance.models.entities import (ExternalAccounts, PaymentType, CoA, Company, RegisterCode, Register)
from MyFinance.models.payables import (AccountsPayable, Liabilities, Periods)

from flask import current_app

import logging,inspect


class PgUtils:
    """This class encapsulates the various functions needed by the finance application

    """
    def __init__(self, pguri):
        self.pguri = pguri
        self.engine = create_engine(pguri)
        self.Session = sessionmaker(self.engine)

    def get_pg_uri(self) -> str:
        """Returns the detected uri
        Returns:
            str: the textual URI to the postgresz
        """
        return self.pguri

    def get_voucher(self, voucher_number : int) -> dict:
        """gets the voucher and vourcher details in JSON format for the given voucher_number

        Args:
            voucher_number (int): The voucher number

        Returns:
            A dict object
        """
        with Session(create_engine(self.get_pg_uri())) as session:
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
                voucher_dict["company_name"] = row.Voucher.company.company_name
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
    
    def get_company(self,filter=None) -> list:
        """gets the list of companies

        :param filter: filter text, defaults to None
        :type filter: str, optional
        :return: a list of the companies
        :rtype: list
        """

        company_list = []
        try:
            if filter == None:
                with self.Session() as session: # type: ignore
                    results = session.query(Company).order_by(Company.company_number)
            else:
                with self.Session() as session: # type: ignore
                    results = session.query(Company).where(Company.company_name.ilike(f"%{filter}%"))
            for row in results:
                company = {}
                company['company_name']=row.company_name
                company['id']=row.id
                company_list.append(company)
        except Exception as ex:
            print(ex.args[0])
        return company_list

    def get_vendors(self,filter=None) -> list:
        """gets the list of vendors

        Returns:
            dict: [{vendor_short_desc: vendor_number}, ...]
        """
        vendor_list = []
        try:
            if filter == None:
                with self.Session() as session: # type: ignore
                    results = session.query(Vendors).order_by(Vendors.vendor_short_desc)

            else:
                with self.Session() as session: #type: ignore
                    results = session.query(Vendors).where(Vendors.vendor_short_desc.ilike(f"%{filter}%",))                
                    #stmt = select(Vendors).where(Vendors.vendor_short_desc ILIKE f'%{filter}%')
                    #results = session.execute(stmt)
            for row in results:
                vendor = {}
                vendor["vendor_short_desc"] = row.vendor_short_desc
                vendor["vendor_number"] = row.vendor_number
                vendor_list.append(vendor)
        except Exception as ex:
            #current_app.logger.error(f'Error in get_vendors: {ex.args[0]}')
            print(ex.args[0])

        return vendor_list

    def get_external_accounts(self) -> list:
        """gets the list of external accounts

        Returns:
            disc: [{account_name: external_account_id}, ...]
        """
        account_list = []
        try:
            with self.Session.begin() as session:  # type: ignore
                results = session.query(ExternalAccounts).order_by(ExternalAccounts.account_name)

                for row in results:
                    account = {}
                    account["account_name"] = row.account_name
                    account["external_account_id"] = row.external_account_id
                    account_list.append(account)
        except Exception as ex:
            print(f"Exception in get_external_accounts: {ex.args[0]}")
            return account_list

        return account_list

    def get_voucher_types(self) -> list:
        """gets the list of voucher types

        Returns:
            list: [{type_text, type_code}, ...]
        """
        voucher_types = []
        try:
            with Session(create_engine(self.get_pg_uri())) as session:  # type: ignore
                results = session.query(VoucherType).order_by(VoucherType.type_text)

                for row in results:
                    type = {}
                    type["type_text"] = row.type_text
                    type["type_code"] = row.type_code
                    voucher_types.append(type)
        except Exception as ex:
            print(f"get_voucher_types: An exception of type {ex} occurred. Arguments:\n{ex.args}")
        

        return voucher_types

    def get_payment_types(self) -> list:
        """gets the list of payment types

        Returns:
            list: [{payment_type_text: payment_type_id}, ...]
        """
        payment_types = []
        try:
            with Session(create_engine(self.get_pg_uri())) as session:  # type: ignore
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
            with Session(create_engine(self.get_pg_uri())) as session: # type: ignore
                session.add(Voucher)
                session.commit()
                session.refresh(Voucher)
                return Voucher.voucher_number
        except Exception as ex:
            logging.error(f'Error in {__name__}:  {ex.args[0]}')
            return f'Error in {__name__}:  {ex.args[0]}'

    def add_voucher_details(self, VoucherDetail):
        try:
            with Session(create_engine(self.get_pg_uri())) as session: # type: ignore
                session.add(VoucherDetail)
                session.commit()
                session.refresh(VoucherDetail)
                return VoucherDetail.id
        except Exception as ex:
            logging.error(f'Error in {__name__}:  {ex.args[0]}')
            return f'Error in {__name__}:  {ex.args[0]}'

    def get_next_split_number(self, voucher_number : int):

        try:
            with Session(create_engine(self.get_pg_uri())) as session: # type: ignore
                result = session.query(VoucherDetail.id).where(VoucherDetail.voucher_number == voucher_number)
                return len(result.all()) + 1 
        except (Exception):
            print(f"Exception in get_next_split_number: {Exception}")
            return -1
                
    def get_detail_total(self, voucher_number : int):
        try:
            with Session(create_engine(self.get_pg_uri())) as session: # type: ignore
                result = session.query(func.sum(VoucherDetail.amount)).where(VoucherDetail.voucher_number==voucher_number)
                if result.scalar() == None:
                    return 0
                else: 
                    return result.scalar()
        except Exception:
            print(f"Exception in get_detail_total: {Exception}")
            return 0

    def add_user(self, username : str, password : str) -> int:
        """add user to user table

        Args:
            username (str): user name
            password (str): user password

        Returns:
            int: a positive number indicating the newly created user id, or -1 if the user exists

        """

        try:
            with Session(create_engine(self.get_pg_uri())) as session:
                # See if the user exists
                results = session.query(User).where(User.username == username)
                if len(results.all()) != 0:
                    return -1
                # user didn't exist, continue to add
                user = User(username=username, password=password)
                session.add(user)
                session.commit()
                session.refresh(user)
                return user.id.cast(int)
        except Exception:
            print(f"Exception in add_user:  {Exception}")
            return -2

    def get_user_by_name(self, username: str) -> dict:
        """get the user based on the username, returns the User model if found, else None

        Args:
            username (str): the username

        Returns:
            dict: User object expressed as a dictionary
        """
        user_dict = {}
        try:
            with Session(create_engine(self.get_pg_uri())) as session:
                results = session.query(User).where(User.username == username)
                for row in results:
                    user_dict['id'] = row.id
                    user_dict['username'] = row.username
                    user_dict['password'] = row.password
        except Exception as ex:
            print(f"Exception in get_user_by_name: {ex.args[0]}")
        return user_dict
        
    def get_user_by_id(self, user_id : int) -> dict:
        """_summary_

        Args:
            user_id (int): _description_

        Returns:
            dict: User object expressed as a dictionary
        """  
        user_dict = {}
        try:
            with Session(create_engine(self.get_pg_uri())) as session:
                results = session.query(User).where(User.id == user_id)
                for row in results:
                    user_dict['id'] = row.id
                    user_dict['username'] = row.username
                    user_dict['password'] = row.password
        except Exception:
            print(f"Exception in get_user_by_id {Exception}")
        return user_dict
    
    #####
    ## Payables
    #####

    def get_payable(self, payable_id) -> dict:
        """gets AccountPayable by id

        :param payable_id: the id of the payable to display
        :type payable_id: integer
        :return: dictionary of payables
        :rtype: dict
        """
        payable_dict = {}
        try:
            with Session(create_engine(self.get_pg_uri())) as session:
                #results = session.query(AccountsPayable).where(AccountsPayable.id == payable_id)
                stmt = select(AccountsPayable.id, Vendors.vendor_short_desc, AccountsPayable.invoice_id, 
                        AccountsPayable.stmt_dt, AccountsPayable.stmt_amt, AccountsPayable.payment_due_dt,
                        ExternalAccounts.account_name,
                        AccountsPayable.payment_voucher_id).join(ExternalAccounts).join(Vendors).where(AccountsPayable.id == payable_id)
                results = session.execute(stmt)
                for row in results:
                    payable_dict['id'] = row.id
                    payable_dict['vendor_short_desc'] = row.vendor_short_desc
                    payable_dict['invoice_id'] = row.invoice_id
                    payable_dict['stmt_dt'] = row.stmt_dt
                    payable_dict['stmt_amt'] = row.stmt_amt
                    payable_dict['payment_due_dt'] = row.payment_due_dt
                    payable_dict['payment_source'] = row.account_name
                    payable_dict['payment_voucher_id'] = row.payment_voucher_id
        except Exception as ex:
            current_app.logger.error(f'Error in get_payable: {ex.args[0]}')

        return payable_dict
    
    def get_payable_by_vendor(self, vendor_number : int) -> list:
        """gets a list of accounts_payable by account number

        :param account_number: the account number being sought
        :type vendor_number: integer
        :return: list of payables
        :rtype: list
        """
        payables_list = []
        try:
            with self.Session() as session:
                stmt = select(AccountsPayable.id, Vendors.vendor_short_desc, AccountsPayable.invoice_id,
                    AccountsPayable.stmt_dt, AccountsPayable.stmt_amt,AccountsPayable.payment_due_dt, ExternalAccounts.account_name,
                    AccountsPayable.payment_voucher_id).join(ExternalAccounts).join(Vendors).where(AccountsPayable.vendor_number== vendor_number).order_by(AccountsPayable.payment_due_dt)
                #print(stmt)
                results = session.execute(stmt)
                for row in results:
                    tmp = {}
                    tmp['id'] = row.id
                    tmp['vendor'] = row.vendor_short_desc
                    tmp['invoice_id'] = row.invoice_id
                    tmp['stmt_dt'] = row.stmt_dt
                    tmp['stmt_amt'] = row.stmt_amt
                    tmp['payment_due_dt'] = row.payment_due_dt
                    tmp['account_name'] = row.account_name
                    tmp['payment_voucher_id'] = row.payment_voucher_id
                    payables_list.append(tmp)        
        except Exception as ex:
            current_app.logger.error(f'{inspect.stack()[0][0].f_code.co_name}: {ex.args[0]}')

        return payables_list

    def add_payable(self, payable : AccountsPayable) -> int:
        try:
            with Session(create_engine(self.get_pg_uri())) as session: # type: ignore
                session.add(payable)
                session.commit()
                session.refresh(payable)
                return payable.id  #type: ignore
        except Exception as ex:
            current_app.logger.error(f'Error in add_payable: {ex.args[0]}')
            return 0
        

    ######
    ## Liabilities
    ######
    def get_liability(self, liability_id : int) -> dict:
        """gets liability by id

        :param liability_id: the id of the payable to display
        :type liability: integer
        :return: dictionary of liability
        :rtype: dict
        """
        liability_dict = {}
        try:
            with Session(create_engine(self.get_pg_uri())) as session:
                #results = session.query(Liabilities).where(Liabilities.id == liability_id)
                stmt = select(Liabilities.id, ExternalAccounts.account_name, Liabilities.original_amt, 
                    Liabilities.current_balance_amt, Liabilities.current_balance_dt, Liabilities.pmt_due_amt,
                    Liabilities.pmt_due_dt, Liabilities.payment_voucher_id, 
                    Liabilities.period_int).join(ExternalAccounts).where(Liabilities.id == liability_id)
                results = session.execute(stmt)
                for row in results:
                    liability_dict['id'] = row.id
                    liability_dict['account_name'] = row.account_name
                    liability_dict['original_amt'] = row.original_amt
                    liability_dict['current_balance_amt'] = row.current_balance_amt
                    liability_dict['current_balance_dt'] = row.current_balance_dt
                    liability_dict['pmt_due_amt'] = row.pmt_due_amt
                    liability_dict['pmt_due_dt'] = row.pmt_due_dt
                    liability_dict['payment_voucher_id'] = row.payment_voucher_id
                    liability_dict['period_int'] = row.period_int
        except Exception as ex:
            current_app.logger.error(f'Error in get_liability: {ex.args[0]}')
        return liability_dict

    def get_liability_by_account(self, account_number : int) -> list:
        """gets liability by account_number

        :param vendor_number: the account number being sought
        :type vendor_number: integer
        :return: list of liabilities
        :rtype: list
        """        
        Liabilities_list = []
        try:
            with Session(create_engine(self.get_pg_uri())) as session:
                stmt = select(Liabilities.id, ExternalAccounts.account_name, Liabilities.original_amt, 
                            Liabilities.current_balance_amt, Liabilities.current_balance_dt,
                            Liabilities.pmt_due_amt, Liabilities.pmt_due_dt, Liabilities.payment_voucher_id,
                            Liabilities.period_int).join(ExternalAccounts).where(ExternalAccounts.external_account_id == account_number)
                print(stmt)
                results = session.execute(stmt)
                for row in results:
                    tmp = {}
                    tmp['id'] = row.id
                    tmp['account_name'] = row.account_name
                    tmp['original_amt'] = row.original_amt
                    tmp['current_balance_amt'] = row.current_balance_amt
                    tmp['current_balance_dt'] = row.current_balance_dt
                    tmp['pmt_due_amt'] = row.pmt_due_amt
                    tmp['pmt_due_dt'] = row.pmt_due_dt
                    tmp['payment_voucher_id'] = row.payment_voucher_id
                    tmp['period_int'] = row.period_int
                    Liabilities_list.append(tmp)  
        except Exception as ex:
            current_app.logger.error(f'Error in get_liability_by_account: {ex.args[0]}')       
            #print(ex.args[0])     
        return Liabilities_list
    
    def add_liability(self, liability : Liabilities) -> int:
        try:
            with self.Session.begin() as session:                
                session.add(liability)
                return 1
        except Exception as ex:
            current_app.logger.error(f'Error in add_liability: {ex.args[0]}')   
            return -1  

    def get_next_liability_id(self) -> int: #type: ignore
        try:
            with self.Session() as session:
                return session.execute(Sequence(name='liabilities_id_seq', schema='finance')) #type: ignore
        except Exception as ex:
            current_app.logger.error(f'Error in get_next_liability_id: {ex.args[0]}')
            return 0
        
    ######
    ## CoA
    ######
    def get_ledger_account(self, alt_ledger_account : str) -> CoA:
        coa = CoA()
        try:
            with self.Session() as session:
                stmt = select(CoA.account_title, CoA.ledger_account, CoA.alt_ledger_account, CoA.balance,
                    CoA.depth, CoA.category).where(CoA.alt_ledger_account == alt_ledger_account)
                results = session.execute(stmt)
                row = results.one()
                coa.account_title = row[0]
        except Exception as ex:
            current_app.logger.error(f'Error in get_get_ledger_account: {ex.args[0]}')
        return coa
    
    ######
    ## Periods
    ######
    def get_period(self, period_number : int) -> tuple:
        try:
            with self.Session() as session:
                stmt = select(Periods.period_start_dt, Periods.period_end_dt).where(Periods.period_number == period_number)
                results = session.execute(stmt)
                row = results.one()
                return (row[0], row[1])
        except Exception as ex:
            current_app.logger.error(f'Error in get_period: {ex.args[0]}')
            return tuple()
        
    ######
    ## Register
    ######
    def get_codes(self) -> list:
        try:
            code_list = []
            with self.Session() as session:
                stmt = select(RegisterCode.code, RegisterCode.name)
                results = session.execute(stmt)
                for row in results:
                    entry = {}
                    entry['code'] = row[0]
                    entry['name'] = row[1]
                    code_list.append(entry)
            return code_list
        except Exception as ex:
            current_app.logger.error(f'Error get_codes: {ex.args[0]}')
            return []
            
                    
        
        
