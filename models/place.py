#!/usr/bin/python3
"""defines a class that inherits BaseModel"""
from models.base_model import BaseModel


class Place(BaseModel):
    """inherits BaseModel"""

    name = ""
    city_id = ""
    user_id = ""
    description = ""
    number_rooms = ""
    number_bathrooms = ""
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
