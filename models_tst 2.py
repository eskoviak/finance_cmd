"""models.py -- contains the ORM models used in the application

"""
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, MetaData,
                        String, create_engine, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

metadata_obj = MetaData(schema='finance_tst')
Base = declarative_base(metadata=metadata_obj)

class Vendors(Base):
    """The Vendors class--a collection of the system vendors

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "vendors"

    vendor_number = Column(Integer, primary_key=True)
    vendor_short_desc = Column(String(30), nullable=False)
    vendor_address = Column(String(60), nullable=True)

    def __repr__(self):
        return(f"Vendor (vendor_number: {self.vendor_number}, vendor_short_desc: {self.vendor_short_desc}, vendor_addres: {self.vendor_address})")

class VoucherType(Base):
    """The VoucherType class is used to define the type of voucher; it is a FK field from Voucher

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "voucher_type"

    type_code = Column(Integer, primary_key=True)
    type_text = Column(String(25), nullable=False)

    def __repr__(self):
        return(f"VoucherType: (type_code: {self.type_code}, type_text: {self.type_text})")
    

class ExternalAccounts(Base):
    """ExteranlAccounts class

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "external_accounts"

    external_account_id = Column(Integer, primary_key=True)
    account_name = Column(String(20), nullable=False)
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
    
class Voucher(Base):
    """Voucher Class

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "voucher"

    voucher_number = Column(Integer, primary_key=True)
    voucher_date = Column(DateTime, nullable=False)
    voucher_ref = Column(String(50), nullable=True)
    voucher_amt = Column(Float, nullable=False)
    voucher_type_id = Column(None, ForeignKey("voucher_type.type_code") )
    voucher_type = relationship("VoucherType")
    vendor_number = Column(None, ForeignKey("vendors.vendor_number"))
    vendor = relationship("Vendors")
    payment_type_id = Column(None, ForeignKey("payment_type.payment_type_id"))
    payment_type = relationship("PaymentType")
    payment_ref = Column(String(50), nullable=True)
    payment_source_id = Column(None, ForeignKey("external_accounts.external_account_id"))
    payment_source = relationship("ExternalAccounts")
    details = relationship("VoucherDetail", back_populates="voucher")

    def __repr__(self):
        return f"Voucher: (number; {self.voucher_number}, date: {self.voucher_date}, ref: {self.voucher_ref}, amt: {self.voucher_amt}, type: {self.voucher_type.type_text}, details: {self.details})"

class VoucherDetail(Base):
    """VoucherDetail class

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "voucher_detail"

    id = Column(Integer, primary_key=True)
    voucher_number = Column(None, ForeignKey("voucher.voucher_number"))
    voucher = relationship("Voucher", back_populates="details")
    split_seq_number = Column(Integer, nullable=False)
    account_number = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    dimension_1 = Column(String(20), nullable=True)
    dimension_2 = Column(String, nullable=True)
    memo = Column(Text)

    def __repr__(self):
        return f"Details: (split: {self.split_seq_number}, account: {self.account_number}, amt: {self.amount})"

#####
# Executtion Wrapper -- if this class is executed, any/all classes will be 
# instantiated
#####
if __name__ == '__main__':
    try:
        psycopg_uri = url = 'postgresql://postgres:terces##@localhost:5432/finance'
        engine = create_engine(psycopg_uri)
        #Base.metadata.create_all(engine)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    
