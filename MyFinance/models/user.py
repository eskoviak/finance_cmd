from sqlalchemy import (Column, Integer, String)
#from sqlalchemy.orm import relationship

from MyFinance.models.base import Base

class User(Base):
    """The user table is used to provided authorization to the app

    Args:
        base (_type_): _description_
    """
    __tablename__ = "user"
    __table_args__ = {'schema': 'finance'}

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    first_name=Column(String(30), nullable=True)
    last_name=Column(String(50), nullable=True)
    email=Column(String(75), nullable=True)

    def __repr__(self):
        return f"User:  (id: {self.id}, username: {self.username})" 