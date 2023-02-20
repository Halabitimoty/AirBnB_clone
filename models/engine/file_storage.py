#!/usr/bin/python3
"""
defines a class that serializes objs to JSON
and deserializes JSON to objs
"""
import json
import os
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """serializes objs to JSON and vice versa"""

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        """stores new object in memory"""
        key = obj.__class__.__name__ + '.' + obj.id
        self.__objects[key] = obj

    def save(self):
        """serializes objs in memory"""
        json_dict = {}
        for k, v in self.__objects.items():
            json_dict[k] = v.to_dict()

        with open(self.__file_path, "w", encoding="utf-8") as fd:
            fd.write(json.dumps(json_dict))

    def reload(self):
        """deserializes objs from json path"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as fd:
                r = fd.read()
                if r:
                    json_dict = json.loads(r)
                    for k, v in json_dict.items():
                        self.__objects[k] = eval(v['__class__'])(**v)
