"""
Main application

This module contains the main fastapi application. Whenever there are requests
for database functions, we just call them out through database.py module
"""
import logging
import os
from typing import List
from functools import wraps
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import HTMLResponse
from database import DataBase
from pydantic_models import AddressCreateUpdate, AddressView, Neighbor
from distance import haversine


# Provide a default value in case the environment variables were not set.
API_KEY = os.environ.get("ADDRESS_BOOK_API_KEY", "af594db1058629e02cc37015f1dc612af582a23bb7bac34c01faff147b3663ad")

# Setup logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

description = """
<b>Author:</b> Ian Rae G. Agustin<br>
<b>Overview:</b> This API allows the user to create, read, update, and delete addresses.
"""
app = FastAPI(
    title = "Address Book API",
    description = description
)
db = DataBase()
logger.info("Initializing tables")
DataBase.create_all()

# def validate_api_key(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         api_key = kwargs.get("api_key")
#         if api_key != API_KEY:
#             raise HTTPException(status_code=403, detail="Invalid API key")
#         return func(*args, **kwargs)
#     return wrapper

def validate_api_key(func):
    """
    Validate the api key provided. Throw an Exception when there is no api provided,
    or if it is invalid.
    """
    # use @wraps(func) to preserve the description of the endpoint
    @wraps(func)
    def wrapper(*args, **kwargs):
        # print(kwargs)
        api_key = kwargs.get("x_api_key")
        if api_key == API_KEY:
            return func(*args, **kwargs)
        if api_key is None:
            logging.warning("No api key provided.")
            raise HTTPException(status_code=403, detail="Unauthenticated user")
        else:
            logging.warning("Invalid api key %s", api_key)
            raise HTTPException(status_code=403, detail="Unauthenticated user")
    return wrapper

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    """
    This is the home page. Direct the user to the documentation page.
    Hide the home page in the documentation page.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Address Book API</title>
    </head>
    <body>
        <h1>Welcome to the Address Book API</h1>
        <p>Please see the <a href ="/docs">documentation page</a> to see available end points.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
@app.post("/addresses/", response_model=AddressView)
@validate_api_key
def create_address(address: AddressCreateUpdate, x_api_key:str = Header(...)):
    """
    Creates an address record in the database
    
    """
    db_address = db.create_address(address)
    return db_address

@app.get("/addresses/{uid}", response_model=AddressView)
@validate_api_key
def read_address(uid: str, x_api_key:str = Header(...)):
    """
    Retrieves the address given a particular uid
    """
    db_address = db.read_address(uid)
    if db_address is None:
        logger.warning("uid %s not found", uid)
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.get("/addresses", response_model=List[AddressView])
@validate_api_key
def read_addresses(x_api_key:str = Header(...)):
    """
    Returns a list of addresses from the table
    """
    db_address = db.read_addresses()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{uid}")
@validate_api_key
def update_address(uid: str, address: AddressCreateUpdate, x_api_key:str = Header(...)):
    """
    Updates the address record of the given uid
    """
    db_address = db.update_address(uid, address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    logger.info("%s : Address updated.", uid)
    return "Success"

@app.delete("/addresses/{uid}")
@validate_api_key
def delete_address(uid: str, x_api_key:str = Header(...)):
    """
    Deletes the address given a particular uid
    """
    db.delete_address(uid)
    logger.info("%s : Address deleted.", uid)
    return "Success"

@app.get("/neighbors/", response_model=List[Neighbor])
@validate_api_key
def get_neighbors(lat: float=Query(... , description="latitude", ge=-90, le=90),
                  long: float=Query(... , description="longitude", ge=-180, le=180),
                  distance: int=Query(..., description="distance in kilometers"),
                  x_api_key:str = Header(...)):
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
    