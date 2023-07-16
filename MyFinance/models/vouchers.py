from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, MetaData,
                        String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (relationship, Mapped, mapped_column)

Base = declarative_base(metadata=MetaData(schema='finance'))
from MyFinance.models.entities import ExternalAccounts, PaymentType
from MyFinance.models.vendors import Vendors

from flask import current_app

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
    vendor_number = Column(None, ForeignKey(Vendors.vendor_number))
    vendor = relationship(Vendors)
    payment_type_id = Column(None, ForeignKey(PaymentType.payment_type_id))
    payment_type = relationship(PaymentType)
    payment_ref = Column(String(50), nullable=True)
    payment_source_id = Column(None, ForeignKey(ExternalAccounts.external_account_id))
    payment_source  = relationship(ExternalAccounts)
    details = relationship("VoucherDetail", back_populates="voucher")

    def __repr__(self):
        return f"""Voucher: (number; {self.voucher_number}, date: {self.voucher_date},
         ref: {self.voucher_ref}, amt: {self.voucher_amt}, type: {self.voucher_type_id}, 
         vendor: {self.vendor_number}, payment_type_id: {self.payment_type_id}, 
         payment_source_id: {self.payment_source_id}, payment_ref: {self.payment_ref}, details: {self.details})"""

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