#!/usr/bin/env python3

"""Module to hold routes related to authentication and authorization"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from models.token_blocklist import TokenBlocklist

import schemas
import database
import crud
from auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    oauth2_scheme,
    credentials_exception,
)
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from config import settings

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(database.get_db),
) -> schemas.Token:
    """
    Endpoint to authenticate a user and generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing the username and password.
        db (Session, optional): Database session. Defaults to Depends(database.get_db).

    Returns:
        schemas.Token: Token response containing the access token and refresh token.

    Raises:
        HTTPException: If the username or password is incorrect.

    Examples:
        Example usage to authenticate a user:
        ```python
        {
            "username": "test",
            "password": "test"
        }
        ```
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.phone}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.phone}, expires_delta=refresh_token_expires
    )
    return schemas.Token(
        access_token=access_token, token_type="bearer", refresh_token=refresh_token
    )


@router.post("/token/refresh", response_model=schemas.Token)
async def refresh_token(
    refresh_token: str, db: Session = Depends(database.get_db)
) -> schemas.Token:
    """
    Endpoint to refresh an access token using a refresh token.

    Args:
        refresh_token (str): Refresh token.
        db (Session, optional): Database session. Defaults to Depends(database.get_db).

    Returns:
        schemas.Token: Token response containing the new access token and refresh token.

    Raises:
        credentials_exception: If the refresh token is invalid.

    Examples:
        Example usage to refresh an access token:
        ```python
        {
            "refresh_token": "refresh
        }
        ```
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        phone = payload.get("sub")
        if phone is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=phone)
    except JWTError:
        raise credentials_exception
    try:
        if token_data.username is None:
            raise credentials_exception
        user = crud.get_user_by_phone(db, phone=token_data.username)
        if user is None:
            raise credentials_exception
    except Exception as e:
        print(e)
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.phone}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.phone}, expires_delta=refresh_token_expires
    )
    return schemas.Token(
        access_token=access_token, token_type="bearer", refresh_token=refresh_token
    )


@router.get("/me", response_model=schemas.UserShow)
async def read_users_me(
    current_user: schemas.UserCreate = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    """
    Endpoint to get the details of the currently authenticated user.

    User must be authenticated to access this endpoint.

    Args:
        current_user (schemas.UserCreate, optional): Current authenticated user. Defaults to Depends(get_current_user).
        db (Session, optional): Database session. Defaults to Depends(database.get_db).

    Returns:
        schemas.UserShow: User details.

    Examples:
        Example usage to get the details of the currently authenticated user:
        ```python
        {
            "id": 1
        }
        ```
    """
    return current_user


@router.post("/logout")
async def logout_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
    current_user: schemas.UserCreate = Depends(get_current_user),
):
    """
    Endpoint to log out a user by adding the token to the blocklist.

    User must be authenticated to access this endpoint.

    Args:
        token (str, optional): Access token. Defaults to Depends(oauth2_scheme).
        db (Session, optional): Database session. Defaults to Depends(database.get_db).
        current_user (schemas.UserCreate, optional): Current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        dict: Success message.

    Examples:
        Example usage to log out a user:
        ```python
        {
            "token": "token"
        }
        ```
    """
    TokenBlocklist.save_from_token(token, db)
    return {"detail": "Successfully logged out."}
