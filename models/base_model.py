#!/usr/bin/python3
"""
defines a class that defines all common attr/methods for other classes
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """defines all the cmon attr/methods for other classes"""

    def __init__(self, *args, **kwargs):
        if kwargs:
            objs = ['created_at', 'updated_at']
            for k, v in kwargs.items():
                if k in objs:
                    setattr(self, k, datetime.fromisoformat(v))
                elif k != '__class__':
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        s = f"[{type(self).__name__}] ({self.id}) {self.__dict__}"
        return s

    def save(self):
        """updates the 'updated_at' attr of the obj"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns the dixt representation of the obj"""
        dict_rep = self.__dict__.copy()
        dict_rep['__class__'] = type(self).__name__
        dict_rep['created_at'] = self.created_at.isoformat()
        dict_rep['updated_at'] = self.updated_at.isoformat()

        return dict_rep
