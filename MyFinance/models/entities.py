from sqlalchemy import (Column, Integer, MetaData, String)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema='finance'))

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