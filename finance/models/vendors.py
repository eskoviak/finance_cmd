from sqlalchemy import (Column, Integer, MetaData, String)
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData(schema='finance'))

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
