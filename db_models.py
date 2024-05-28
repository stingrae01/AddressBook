"""
Module for defining database tables.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()
class Address(Base):
    """
    Table for all addresses
    """
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True)    
    country = Column(String, index=True)
    street_name = Column(String)
    street_num = Column(String)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    name = Column(String, index=True) # Descriptive address
