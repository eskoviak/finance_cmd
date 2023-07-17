import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, MetaData, String, Text, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (relationship, Mapped, mapped_column)

from MyFinance.models.entities import ExternalAccounts
from MyFinance.models.vendors import Vendors
from MyFinance.models.vouchers import Voucher

#from sqlalchemy.orm import Session
#from flask import current_app
from datetime import datetime
from pathlib import Path
import os

Base = declarative_base(metadata=MetaData(schema='finance'))

class Liabilities(Base):
    """Liablities Class

        This class is used to model entities which have an initial value and paid over time, such as a loan.  An entity
        which is contractual based (such as a service or subscription) and has a fixed or viable payment should be
        modeled as an account_payable.
    
        :param Base: Metadata base object used by SQLAlchemy to wrap the PostgreSQL database
        :type kind: sqlalchemy.ext.declarative.declarative_base
        
    """

    __tablename__ = 'liabilities'

    #id = Column(Integer, primary_key=True)
    id : Mapped[int] = mapped_column(primary_key=True)
    #external_account_id = Column(None, ForeignKey(ExternalAccounts.external_account_id))
    external_account_id : Mapped[int] = mapped_column(ForeignKey(ExternalAccounts.external_account_id))
    #account_name = relationship(ExternalAccounts)
    #original_amt = Column(Float, nullable=True)
    original_amt : Mapped[float]
    #current_balance_amt = Column(Float, nullable=True)
    current_balance_amt : Mapped[float]
    #current_balance_dt = Column(DateTime, nullable=True)
    current_balance_dt : Mapped[datetime]
    #pmt_due_amt = Column(Float, nullable=False)
    pmt_due_amt : Mapped[float] = mapped_column(nullable=False)
    #pmt_due_dt = Column(DateTime, nullable=False)
    pmt_due_dt : Mapped[datetime] = mapped_column(nullable=False)
    #payment_voucher_id = Column(None, ForeignKey(Voucher.voucher_number))
    payment_voucher_id : Mapped[int] = mapped_column(ForeignKey(Voucher.voucher_number))
    #period_int = Column(Float, nullable=True)
    period_int : Mapped[float]

    def __repr__(self):
        return f"Liability (id: {self.id}, account_name: {self.account_name}, account_name {self.account_name}, ...)"
    
class AccountsPayable(Base):
    """AccountsPayable Class

        This class is used to model entities which have a monthly (periodic) payment, fixed or variable.  There really is
        no concept of current or future value.  Some services, may offer a purchase embedded in the monthly cost--that is not
        modelled separately--it is considered part of the base price.

        An example of the above is a wireless carrier may include the cost of a phone in the montly contract.  That installment
        load is not modeled separately. 

        :param Base: Metadata base object used by SQLAlchemy to wrap the PostgreSQL database
        :type kind: sqlalchemy.ext.declarative.declarative_base

    """

    __tablename__ = 'accounts_payable'

    #id = Column(Integer, primary_key=True)
    id : Mapped[int] = mapped_column(primary_key=True)
    #vendor_number = Column(None, ForeignKey(Vendors.vendor_number))
    vendor_number : Mapped[int] = mapped_column(ForeignKey(Vendors.vendor_number))
    #vendor_short_desc = relationship(Vendors)
    #invoice_id = Column(String, nullable=True)
    invoice_id : Mapped[str]
    #stmt_dt = Column(DateTime, nullable=False)
    stmt_dt : Mapped[datetime] = mapped_column(nullable=False)
    #stmt_amt = Column(Float, nullable=False)
    stmt_amt : Mapped[float] = mapped_column(nullable=False)
    #payment_due_dt = Column(DateTime, nullable=False)
    payment_due_dt : Mapped[datetime] = mapped_column(nullable=False)
    #payment_source_id = Column(None, ForeignKey(ExternalAccounts.external_account_id))
    payment_source_id : Mapped[int] = mapped_column(ForeignKey(ExternalAccounts.external_account_id))
    #payment_source = relationship(ExternalAccounts)
    #payment_voucher_id = Column(None, ForeignKey(Voucher.voucher_number))
    payment_voucher_id : Mapped[int] = mapped_column(ForeignKey(Voucher.voucher_number))
    

    def __repr__(self):
        return f"AccountPayable (id: {self.id}, vendor: {self.vendor_short_desc}, statement_dt: {self.stmt_dt}, statement_amt: {self.stmt_amt}, ...)"
    
class Periods(Base):
    """Periods Class

        The periods class represents the periods in the year by which the accounting system will be configured. This allows analysis by period.

        :param Base: Metadata base object used by SQLAlchemy to wrap the PostgreSQL database
        :type kind: sqlalchemy.ext.declarative.declarative_base
    """

    __tablename__ = 'periods'

    #id = Column(Integer, primary_key=True)
    id : Mapped[int] = mapped_column(primary_key=True)
    #period_number = Column(Integer, nullable=False)
    period_number : Mapped[int] = mapped_column(nullable=False)
    #period_start_dt = Column(DateTime, nullable=False)
    period_start_dt : Mapped[datetime] = mapped_column(nullable=False)
    #period_end_dt = Column(DateTime, nullable=False)
    period_end_dt : Mapped[datetime] = mapped_column(nullable=False)

    def __repr__(self):
        return f'Period: (id: {self.id}, period_number: {self.period_number}, period_start-dt: {self.period_start_dt}, period_end_date: {self.period_end_dt})'

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
        engine = create_engine(os.environ.get('PGURI'))
        Base.metadata.create_all(engine)
    except FileNotFoundError as fnfe:
        print(f'Config file open error: {fnfe.args}')
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))