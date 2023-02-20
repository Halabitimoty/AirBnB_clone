#!/usr/bin/python3
"""defines a class that inherits from BaseModel"""
from models.base_model import BaseModel


class User(BaseModel):
    """defines a user"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
