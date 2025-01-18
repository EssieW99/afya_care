#!/usr/bin/env python3
""" Authentication file"""

from models.user import User
from models.admin_emails import Admin_Emails
from models.db import DB
import bcrypt
import base64
import secrets
from sqlalchemy.orm.exc import NoResultFound



def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password
    """

    """ convert password to array of bytes"""
    password_bytes = password.encode('utf-8')

    """ generate the salt"""
    salt = bcrypt.gensalt()

    """ hashing the password"""
    hashed_passwd = bcrypt.hashpw(password_bytes, salt)

    return hashed_passwd


class Auth:
    """Auth class to interact with the database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, first_name: str, last_name: str, email: str,
                      national_id: str, phone_number: str, password: str, ) -> User:
        """
        registers a new user
        """

        db = self._db

        try:
            user = db.find_user_by(email=email)
            raise ValueError(f'User {user.email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = db.add_user(first_name, last_name, email, national_id, phone_number, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> User:
        """
        credential validation
        """

        db = self._db

        try:
           user = db.find_user_by(email=email)
           passwd_bytes = password.encode('utf-8')
           if bcrypt.checkpw(passwd_bytes, user.hashed_password):
               return user
           else:
               return None
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        finds a user by the session id
        """

        pass


    def destroy_session(self, user_id: int) -> None:
        """
        updates the user's session ID to None
        """
        db = self._db

        if user_id is None:
            return None
        try:
            db.update_user(user_id=user_id, session_id=None)
            return None
        except (NoResultFound, ValueError):
            return None


    def get_reset_password_token(self, email: str) -> str:
        """
        generates a reset password token
        """

        pass


    def update_password(self, reset_token: str, password: str) -> None:
        """
        updates the database with the new password
        """

        pass
