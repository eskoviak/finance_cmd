"""models.py -- contains the ORM models used in the application

"""
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, MetaData,
                        PrimaryKeyConstraint, String, Text, create_engine)
from sqlalchemy.ext.declarative import declarative_base

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
        return(f"Vendor (vendor_number: {self.vendor_number}, vendor_short_desc: {self.vendor_short_desc}, vendor_addres: {self.vendor_address}")

#####
# Executtion Wrapper -- if this class is executed, any/all classes will be 
# instantiated
#####
if __name__ == '__main__':
    try:
        psycopg_uri = url = 'postgresql://postgres:terces##@localhost:5432/finance'
        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    #Base.metadata.create_all(engine)
