"""
Database connection module

This module provides functions to establish connections to the database.
"""
import uuid
from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker

from db_models import Base
from db_models import Address
from pydantic_models import AddressCreateUpdate

DATABASE_URL = "sqlite:///./address_book.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class DataBase():
    """
    Manages all the database functions.
    """
    db = None
    def __init__(self):
        self.db = self.get_db()

    def get_db(self):
        """
        Get database connection. If a connection already exists, return the 
        existing connection. Do not make more connections.
        """
        if self.db is None:
            self.db = SessionLocal()
        return self.db

    @classmethod
    def create_all(cls):
        """
        Create all database tables. 
        """
        Base.metadata.create_all(bind=engine)

    def create_address(self, address: AddressCreateUpdate):
        """
        Creates an address in the database.
        """
        db = self.get_db()
        db_address = Address(uid = str(uuid.uuid4()), name = address.name, country = address.country,
            latitude = address.latitude, longitude = address.longitude,
            street_num = address.street_num, street_name = address.street_name, city = address.city
            )
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address

    def read_address(self, uid):
        """
        Retrieves an address from the database with the specified uid.
        """
        db = self.get_db()
        db_address = db.query(Address).filter(Address.uid == uid).first()
        return db_address

    def read_addresses(self):
        """
        Returns all the addresses in the database.
        """
        db = self.get_db()
        db_address = db.query(Address).all()
        return db_address

    def update_address(self, uid, address: AddressCreateUpdate):
        """
        Retrieves an address from the database with the specified uid.
        """

        stmt = (
            update(Address).
            where(Address.uid == uid).
            values(name = address.name, latitude = address.latitude,
                longitude= address.longitude, city = address.city, 
                street_num = address.street_num,
                street_name = address.street_name,
                country = address.country)
            )
        db = self.get_db()
        db.execute(stmt)
        db.commit()
        db.close()
        return address

    def delete_address(self, uid):
        """
        Deletes an address from the database with the specified uid.
        """

        stmt = (
            delete(Address).
            where(Address.uid == uid)
            )
        db = self.get_db()
        db.execute(stmt)
        db.commit()
        db.close()
        return True
