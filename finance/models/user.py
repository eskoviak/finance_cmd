from sqlalchemy import (Column, Integer, MetaData, String)
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData(schema='finance'))

class User(Base):
    """The user table is used to provided authorization to the app

    Args:
        base (_type_): _description_
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    first_name=Column(String(30), nullable=True)
    last_name=Column(String(50), nullable=True)
    email=Column(String(75), nullable=True)

    def __repr__(self):
        return f"User:  (id: {self.id}, username: {self.username})" 