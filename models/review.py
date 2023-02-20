#!/usr/bin/python3
"""defines a class that inherits BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """inherits BaseModel"""

    place_id = ""
    user_id = ""
    text = ""
