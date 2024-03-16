import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, MetaData, String, Text, create_engine)
from sqlalchemy.orm import (relationship, Mapped, mapped_column, declarative_base)

from MyFinance.models.vendors import Vendors
#from MyFinance.models.vouchers import Voucher

#from sqlalchemy.orm import Session
#from flask import current_app
from datetime import datetime
from pathlib import Path
import os

Base = declarative_base(metadata=MetaData(schema='finance'))

class ExternalAccounts(Base):
    """SQLAlchemy class to model the table `external_accounts`

    :param Base: The base for all SQLAlchemy ORM data classes
    :type Base: sqlalchemy.ext.declarative.declara
    """
    __tablename__ = "external_accounts"

    external_account_id : Mapped[int] = mapped_column(primary_key=True)
    account_name : Mapped[str] = mapped_column(nullable=False)
    account_number : Mapped[str] = mapped_column(nullable=False)
    qualified : Mapped[str]

class PaymentType(Base):
    """PaymentType class represents the types of payment that can be made, such as Credit Card, Cash and ACH.

    :param Base: The base for all SQLAlchemy ORM data classes
    :type Base: sqlalchemy.ext.declarative.declara
    """
    __tablename__ = "payment_type"

    payment_type_id : Mapped[int] = mapped_column(primary_key=True)
    payment_type_text : Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return(f"Payment Type: (payment_type_id: {self.payment_type_id}, payment_type_text: {self.payment_type_text})")
    
class CoA(Base):
    """Chart of accounts class

        :param Base: Metadata base object used by SQLAlchemy to wrap the PostgreSQL database
        :type kind: sqlalchemy.ext.declarative.declarative_base

    """
    __tablename__ = 'coa'

    id : Mapped[int] = mapped_column(primary_key=True)
    account_title : Mapped[str] = mapped_column(nullable=False)
    ledger_account : Mapped[str] = mapped_column(nullable=False)
    alt_ledger_account : Mapped[str] = mapped_column(nullable=False)
    depth : Mapped[int] = mapped_column(nullable=False)
    balance : Mapped[str] = mapped_column(nullable=False)
    category : Mapped[str]
    dimension_1 : Mapped[str]
    dimension_2 : Mapped[str]

    def __repr__(self):
        return f"CoA: (id: {self.id}, Account Title: {self.account_title}, Account Number: {self.ledger_account}, alt_ledger_account: {self.alt_ledger_account}, depth: {self.depth}, balance: {self.balance}, category: {self.category}\n)"


class Company(Base):
    """Company codes class

        :param Base: Metadata base object used by SQLAlchemy to wrap the PostgreSQL database
        :type kind: sqlalchemy.ext.declarative.declarative_base
    
    """
    __tablename__ = 'company'

    id : Mapped[int] = mapped_column(primary_key=True)
    company_number : Mapped[int] = mapped_column(nullable=False)
    company_name : Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Company Name: {self.company_name}; Company Number: {self.company_number}"
    
class RegisterCode(Base):
    """RegisterCode Class -- used to indicate the type of entry in the register

        :param Base: Metadata base object used by SQLAlchemy to wrap the PostgreSQL database
        :type kind: sqlalchemy.ext.declarative.declarative_base
      
    """
    __tablename__ = 'register_code'
    code: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class Register(Base):
    """Register Class -- used to represent a register for cash based asset classes, such as a checking account,
       to record transactions.

        :param Base: Metadata base object used by SQLAlchemy to wrap the PostgreSQL database
        :type kind: sqlalchemy.ext.declarative.declarative_base
        
    """
    
    __tablename__ = 'register'
    
    id : Mapped[int] = mapped_column(primary_key=True)
    external_account_id : Mapped[int] = mapped_column(ForeignKey(ExternalAccounts.external_account_id))
    code : Mapped[int] = mapped_column(ForeignKey(RegisterCode.code))
    date : Mapped[datetime] = mapped_column(nullable=False)
    description : Mapped[str] = mapped_column(nullable = True)
    debit : Mapped[float] = mapped_column(nullable=True)
    isFee : Mapped[bool] = mapped_column(default=False)
    credit : Mapped[float] = mapped_column(nullable=True)
    tran_no : Mapped[int] = mapped_column(nullable=True)
    
    def __repr__(self):
        return f"""Id: {self.id}, Ext Acct Id: {self.external_account_id}, Code: {self.code}, Date: {self.date}
Desc: {self.description}, Debit: {self.debit}, Fee: {self.isFee}, Credit: {self.credit}, Tran#: {self.tran_no}
    
        """
    
    

#####
# Execution Wrapper -- if this class is executed, any/all classes will be 
# instantiated/modified
#####
if __name__ == '__main__':
    try:
        #config = {}
        #home = Path(os.environ['HOME']+'/Documents/repos/finance_cmd')
        #print(home)
        #f = open( home / 'instance' / 'config.py')
        #for line in f.readlines():
        #    s = line.split('=')
        #    config[s[0]] = s[1].replace("'",'').replace('\n', '')        
        #engine = create_engine(config['PGURI'])
        engine = create_engine(os.environ.get('PG_LOCAL')+'finance') #type: ignore
        Base.metadata.create_all(engine)
    #except FileNotFoundError as fnfe:
    #    print(f'Config file open error: {fnfe.args}')
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))