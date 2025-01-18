from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base



class Admin_Emails(BaseModel):
    """ A claims table """

    __tablename__ = 'admin_emails'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String(50), unique=True)
