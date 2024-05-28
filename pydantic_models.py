"""
Pydantic Models

This module contains functions for data validation and serialization.

"""
from pydantic import BaseModel, Field
from pydantic import validator

class Address(BaseModel):
    """
    Base class for an Address
    """
    name: str= Field(..., example = "Descriptive name of the place.")
    latitude: float = Field(..., example = 40.6970193)
    longitude: float = Field(..., example = -74.3093317)
    street_num: str = ""
    street_name: str = ""
    city: str = ""
    country: str = ""

    @validator('latitude')
    @classmethod
    def latitude_must_be_in_range(cls, val):
        """
        Latitude must be from -90 to 90
        """
        if -90 <= val <= 90 :
            return val
        else:
            raise ValueError('latitude must be from -90 to 90')

    @validator('longitude')
    @classmethod
    def longitude_must_be_in_range(cls, val):
        """
        Longitude must be from -180 to 180
        """
        if -180 <= val <= 180 :
            return val
        else:
            raise ValueError('longitude must be from -180 to 180')
    class Config:
        orm_mode = True

class AddressCreateUpdate(Address):
    """
    Class for Creating and updating addresses. For now, we only inherit from
    the base Address class. There maybe a time when we need to add more fields
    here.
    """


class AddressView(Address):
    """
    Class for serializing addresses for retrieval. Include the uid
    """
    uid: str

class Neighbor(AddressView):
    """
    Class for serializing neighboring addresses. Additional field distance
    """
    distance: float