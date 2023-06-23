#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from sqlalchemy import Column,String
from sqlalchemy.orm import relationship
from models import storage_type
class User(BaseModel):
    """This class defines a user by various attributes"""
    if storage_type == 'db':
        __tablename__ = "users"
        email = Column(String(128),nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
