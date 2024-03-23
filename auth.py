#!/usr/bin/env python3

"""Module to hold routes relate authentication and authorisation"""

import uuid
from typing import Annotated, Any, Union
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

import crud
from models.token_blocklist import TokenBlocklist
import schemas
from database import get_db
from models.user import Hasher, User
from config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

blocklisted_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Logged out.",
    headers={"WWW-Authenticate": "Bearer"},
)


def authenticate_user(db: Session, phone: str, password: str):
    """
    Authenticates a user by checking if the provided phone and password
      match a user in the database.

    Args:
        db (Session): The database session.
        phone (str): The phone of the user.
        password (str): The password of the user.

    Returns:
        Union[User, bool]: The authenticated user if the phone and password match,
          False otherwise.
    """
    user = crud.get_user_by_phone(db, phone)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    """
    Create an access token.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta, optional): The expiration time delta for the token.
          Defaults to None.

    Returns:
        str: The encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    """
    Create a refresh token.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta, optional): The expiration time delta for the token.
          Defaults to None.

    Returns:
        str: The encoded refresh token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    """
    Retrieves the current user based on the provided token.

    Args:
        token (str): The authentication token.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The current user.

    Raises:
        credentials_exception: If the token is invalid or the user does not exist.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # check if token is blacklisted
        jti: str = payload.get("jti", None)
        if TokenBlocklist.is_jti_blocklisted(jti, db):
            raise blocklisted_token_exception
        username: Any | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_phone(db, phone=username)
    if user is None:
        raise credentials_exception
    return user
