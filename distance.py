"""
This module computes for the distance between 2 points in the earth
"""
import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Function to compute the distance of two places given latitude and longitude values.
    
    a = sin²(φB - φA/2) + cos φA * cos φB * sin²(λB - λA/2)
    c = 2 * atan2( √a, √(1−a) )
    d = R * c
    """

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Radius of Earth in kilometers. Use 3956 for miles
    R = 6371.0
    distance = R * c
    
    return distance
