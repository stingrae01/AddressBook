"""
Main application

This module contains the main fastapi application. Whenever there are requests
for database functions, we just call them out through database.py module
"""
import logging
from typing import List
from fastapi import FastAPI, HTTPException, Query
from database import DataBase
from pydantic_models import AddressCreateUpdate, AddressView, Neighbor
from distance import haversine

# Setup logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


app = FastAPI()
db = DataBase()
logger.info("Initializing tables")
DataBase.create_all()

@app.post("/addresses/", response_model=AddressView)
def create_address(address: AddressCreateUpdate):
    """
    Creates an address record in the database
    
    """
    db_address = db.create_address(address)
    return db_address

@app.get("/addresses/{uid}", response_model=AddressView)
def read_address(uid: str):
    """
    Retrieves the address given a particular uid
    """
    db_address = db.read_address(uid)
    if db_address is None:
        logger.warning("uid {} not found".format(uid))
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.get("/addresses", response_model=List[AddressView])
def read_addresses():
    """
    Returns a list of addresses from the table
    """
    db_address = db.read_addresses()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{uid}")
def update_address(uid: str, address: AddressCreateUpdate):
    """
    Updates the address record of the given uid
    """
    db_address = db.update_address(uid, address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    logger.info("{} : Address updated.".format(uid))
    return "Success"

@app.delete("/addresses/{uid}")
def delete_address(uid: str):
    """
    Deletes the address given a particular uid
    """
    db.delete_address(uid)
    logger.info("{} : Address deleted.".format(uid))
    return "Success"

@app.get("/neighbors/", response_model=List[Neighbor])
def get_neighbors(lat: float=Query(... , description="latitude", ge=-90, le=90 ),
                  long: float=Query(... , description="longitude", ge=-180, le=180 ),
                  distance: int=Query(..., description="distance in kilometers")):
    """
    Retrieve the addresses that are within a given distance and location coordinates.
    """

    distances = []
    for a in db.read_addresses():
        dist = haversine(lat, long, a.latitude, a.longitude)
        n = Neighbor(name = a.name, uid = a.uid,
            latitude = a.latitude, longitude = a.longitude,
            street_num = a.street_num, street_name = a.street_name,
            city = a.city, country = a.country, distance = dist)
        if n.distance <= distance:
            distances.append(n)
    return distances
    