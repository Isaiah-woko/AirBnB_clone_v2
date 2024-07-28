#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_ob
import models
from models.city import City


class State(BaseModel, Base):
    """ State class """
    if storage_ob == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def cities_list(self):
        """return the cities"""
        if storage_ob != 'db':
            all_cities = models.storage.all(City)
            cities_status = [c for c in all_cities.values() 
                             if c.state_id == self.id]
            return cities_status
        return []
