#!/usr/bin/env python3
""" User class"""


from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


class User(BaseModel):
    """ a User class"""

    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    national_id = Column(String(8), unique=True, nullable=False)
    phone_number = Column(String(15), nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    session_id = Column(String(5), nullable=True)
    reset_token = Column(String(5), nullable=True)
    claims = relationship('Claims', back_populates='user')
