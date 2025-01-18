#!/usr/bin/env python3
""" contains the Base Model Class """

from datetime import datetime, timezone
import sqlalchemy
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class BaseModel(Base):
    """
    BaseModel class from which future classes will inherit
    """

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)



    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def to_dict(self):
        """ converts instance attributes to a dictionary"""

        dict_repr = {key: value if not isinstance(value, datetime) else value.isoformat()
                     for key, value in self.__dict__.items() if not key.startswith('_')}
        return dict_repr
