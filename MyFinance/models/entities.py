import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, MetaData, String, Text, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from MyFinance.models.vendors import Vendors
#from MyFinance.models.vouchers import Voucher

#from sqlalchemy.orm import Session
#from flask import current_app
from pathlib import Path
import os

Base = declarative_base(metadata=MetaData(schema='finance'))

class ExternalAccounts(Base):
    """ExteranlAccounts class

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "external_accounts"

    external_account_id = Column(Integer, primary_key=True)
    account_name = Column(String(100), nullable=False)
    account_number = Column(String(10), nullable=False)
    qualified = Column(String(1), nullable=True)

class PaymentType(Base):
    """PaymentType class

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "payment_type"

    payment_type_id = Column(Integer, primary_key=True)
    payment_type_text = Column(String(20), nullable=False)

    def __repr__(self):
        return(f"Payment Type: (payment_type_id: {self.payment_type_id}, payment_type_text: {self.payment_type_text})")
    
class CoA(Base):
    """Chart of accounts class

        :param Base: Metadata base object used by SQLAlchemy to wrap the PostgreSQL database
        :type kind: sqlalchemy.ext.declarative.declarative_base

    """
    __tablename__ = 'coa'

    id = Column(Integer, primary_key=True)
    account_title = Column(String(100), nullable=False)
    ledger_account = Column(String(15), nullable=False)
    alt_ledger_account = Column(String(15), nullable=False)
    depth = Column(Integer, nullable=False)
    balance = Column(String(12), nullable=False)
    category = Column(Text, nullable=True)

    def __repr__(self):
        return f"CoA: (id: {self.id}, account_title: {self.account_title}, ledger_account: {self.ledger_account}, alt_ledger_account: {self.alt_ledger_account}, depth: {self.depth}, balance: {self.balance}, category: {self.category}\n)"

#####
# Execution Wrapper -- if this class is executed, any/all classes will be 
# instantiated/modified
#####
if __name__ == '__main__':
    try:
        config = {}
        home = Path(os.environ['HOME']+'/Documents/repos/finance_cmd')
        print(home)
        f = open( home / 'instance' / 'config.py')
        for line in f.readlines():
            s = line.split('=')
            config[s[0]] = s[1].replace("'",'').replace('\n', '')        
        engine = create_engine(config['PGURI'])
        Base.metadata.create_all(engine)
    except FileNotFoundError as fnfe:
        print(f'Config file open error: {fnfe.args}')
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))