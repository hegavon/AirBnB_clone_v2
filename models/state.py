#!/usr/bin/python3
"""Defines the State class."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv
import models


class State(BaseModel, Base):
    """Represents a state."""

    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete-orphan", backref="state")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Get a list of all related City objects."""
            city_list = []
            for city in list(models.storage.all(models.City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

    def __init__(self, *args, **kwargs):
        """Initializes a state."""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """Returns the string representation of the state."""
        return f"<State {self.id}>"
