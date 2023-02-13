#!/usr/bin/python3
"""
Class that defines a state
"""
from models.base_model import BaseModel


class State(BaseModel):
    """class to create a state
     Attributes:
        name (str): The name of the state.
    """
    
    name = ""
