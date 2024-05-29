import pytest
from db_models import Address
from pydantic_models import AddressCreateUpdate
from database import DataBase

def test_crud_address():
    db = DataBase()
    
    address = AddressCreateUpdate(name = "Test Name", street_num = "123", 
    street_name = "Bloomfield Ave", city= "Montclair", 
    latitude = 40.82442818040041, longitude = -74.21291214528885,
    country = "USA")    

    db_address = db.create_address(address = address)
    uid = db_address.uid
    assert uid is not None
    assert db_address.name == address.name
    assert db_address.street_num == address.street_num
    assert db_address.street_name == address.street_name
    assert db_address.latitude == address.latitude
    assert db_address.longitude == address.longitude
    assert db_address.country == address.country

    db_address = db.read_address(uid)
    assert db_address is not None    
    str_name = "Fairview Lane"
    address.street_name = str_name
    db.update_address(uid, address)
    db_address = db.read_address(uid)
    assert db_address.street_name == str_name
    
    db.delete_address(uid)
    db_address = db.read_address(uid)
    assert db_address is None
