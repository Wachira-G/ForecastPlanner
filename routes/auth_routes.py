#!/usr/bin/env python3

"""Module to hold routes relate authentication and authorisation"""

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
    print(
        "decoded refresh_token: ",
        jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM),
    )
    print(
        "decoded access_token: ",
        jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM),
    )
    return schemas.Token(
        access_token=access_token, token_type="bearer", refresh_token=refresh_token
    )


@router.get("/me", response_model=schemas.UserShow)
async def read_users_me(
    current_user: schemas.UserCreate = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    return current_user


@router.post("/logout")
async def logout_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
    current_user: schemas.UserCreate = Depends(get_current_user),
):
    TokenBlocklist.save_from_token(token, db)
    return {"detail": "Successfully logged out."}
