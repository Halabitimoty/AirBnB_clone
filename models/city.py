#!/usr/bin/python3
"""defines a class that inherits BaseModel"""
from models.base_model import BaseModel


class City(BaseModel):
    """inherits BaseModel"""

    name = ""
    state_id = ""
