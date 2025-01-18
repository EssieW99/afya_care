#!/usr/bin/env python3
""" model forr the claims table"""

from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, LargeBinary, Text, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Claims(BaseModel):
    """ A claims table """

    __tablename__ = 'Claims'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    claim_date = Column(Date, nullable=False)
    claim_type = Column(String(50), nullable=False)
    claim_amount = Column(Float, nullable=False)
    documents = Column(Text, nullable=True)
    status = Column(String(20), default='Pending')
    review_message = Column(String(250), nullable=True)

    user = relationship('User', back_populates='claims')
    