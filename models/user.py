#!/usr/bin/python3
"""This is model defines a class user"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Represents a user in the system."""

    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))

    places = relationship(
        "Place",
        cascade="all, delete-orphan",
        backref="user"
    )
    reviews = relationship(
        "Review",
        cascade="all, delete-orphan",
        backref="user"
    )

    def __init__(self, *args, **kwargs):
        """Initializes a user."""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """Returns the string representation of the user."""
        return f"<User {self.id}>"
