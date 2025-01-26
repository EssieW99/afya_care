#!/usr/bin/env python3
"""DB module
"""

import bcrypt
from models.base_model import Base
from models.claims import Claims
from models.admin_emails import Admin_Emails
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from models.user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Dict, Any
from dotenv import load_dotenv
import os



class DB:
    """ interacts with the PostgreSQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """ instance of a DBStorage object"""

        """ load env variables from .env file"""
        load_dotenv()

        """ retrieve database credentials"""
        POSTGRES_USER = os.getenv('POSTGRES_USER')
        POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        POSTGRES_DB = os.getenv('POSTGRES_DB')

        try:
            """ create an engine for postgreSQL"""
            self.__engine = create_engine(
                f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
            )

            connect = self.__engine.connect()
            from sqlalchemy.sql import text
            query = text("SELECT 1")
            result = connect.execute(query)
            print("Database connection successful!")

            Base.metadata.create_all(self.__engine)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the database: {e}")

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self.__engine)
            self.__session = DBSession()
        return self.__session

    def save(self):
        """ commits to the database"""

        session = self._session
        session.commit()

    def add_user(self, first_name: str, last_name: str, email: str,
                 national_id: str, phone_number: str, hashed_password: str) -> User:
        """
        saves the user to the database.
        """

        new_user = User(first_name=first_name, last_name=last_name, email=email,
                        national_id=national_id, phone_number=phone_number, hashed_password=hashed_password)

        session = self._session
        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        finds a user by the use of arbitrary keyword arguments
        """

        session = self._session

        try:

            user = session.query(User).filter_by(**kwargs).first()

            if not user:
                raise NoResultFound()
            return user
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        locates a user then updates the user's attributes
        as passed in the method's arguments
        """

        session = self._session
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("Error")

            setattr(user, key, value)

        session.commit()
        return None
    
    def is_email_for_admin(self, email):
        """
        checks if the email inputed belongs to an admin
        """
        
        print(f"Checking if {email} is an admin email")
        session = self._session
        admin_email = session.query(Admin_Emails).filter_by(email=email).first()
        print(f"Checking admin status for email: {email}")
        print(f"is_email_for_admin result: {(email)}")

        return admin_email is not None

    def save_claim(self, user_id, claim_date, claim_type, claim_amount, documents):
        """ saves a claim to the database"""

        new_claim = Claims(user_id=user_id, claim_date=claim_date, claim_type=claim_type, claim_amount=claim_amount, documents=documents)
        session = self._session
        session.add(new_claim)
        session.commit()
        return new_claim
    
    def get_claims_by_user(self, user_id):
        """
        gets all the claims madeby a user
        """

        session = self._session
        return session.query(Claims).filter_by(user_id=user_id).all()

    def get_claim_by_id(self, id):
        """
        retrieves a claim based of its ID
        """
        
        session = self._session
        return session.query(Claims).filter_by(id=id).first()
    
    def get_claims_by_type(self, claim_type):
        """
        gets all the claims under a certain type
        """

        session = self._session
        return session.query(Claims).filter_by(claim_type=claim_type, status='Pending').all()
    
    def get_all_claims(self):
        """
        gets all the claims
        """

        session = self._session
        return session.query(Claims).filter_by(status='Pending').all()

    def save_claim_update(self, claim_id, new_status, new_message):
        """
        saves the updated status and review_message of a pending claim report
        """

        session = self._session

        claim = session.query(Claims).filter_by(id=claim_id).first()
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404

        claim.status = new_status
        claim.review_message = new_message

        try:
            session.commit()
            return claim
        except Exception as e:
            session.rollback()
            print(f"Error saving claim status update: {e}")
            return None