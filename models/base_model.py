#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


if models.storage_ob == "db":
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    """A base class for all hbnb models"""
    def __init__(self, *args, **kwargs):
        """
        *args, **kwargs arguments for the constructor of a BaseModel
        """
        # i updated the class attrbutes id, created_at and updated_at\
        # based on requirements. I have also backed up your original code
        # elsewhere incase you need to make changes\

        self.id = Column(String(60), primary_key=True, nullable=False,
                         default=str(uuid.uuid4()))
        self.created_at = Column(DateTime, nullable=False,
                                 default=datetime.now)
        self.updated_at = Column(DateTime, nullable=False,
                                 default=datetime.now)  # I think this doesn't\
        # need to exist in the requirement: otherwise:\
        # create id and created_at as you did previously (new instance)
        if kwargs:
            # Iterate through kwargs
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ['created_at', 'updated_at']:
                    setattr(self, key,
                            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
            if "__class__" in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at
        dictionary['updated_at'] = self.updated_at
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        models.storage.delete(self)
