#!/usr/bin/env python3


"""Module to hold routes relate to users"""

from typing import Generator, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import auth
from database import get_db

router = APIRouter()


# create a user
@router.post("/users", response_model=schemas.UserShow)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user or db_user_email:
        raise HTTPException(
            status_code=400, detail="Credentials already registered (email or phone)"
        )
    return crud.create_user(db=db, user=user)


# get all users (default = 100)
@router.get("/users", response_model=List[schemas.UserShow])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserShow = Depends(auth.get_current_user),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# get a user by their id
@router.get("/users/{user_id}", response_model=schemas.UserShow)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserShow = Depends(auth.get_current_user),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


""" @router.get("/users/{user_email}", response_model=schemas.UserShow)
def read_user(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user """

# update a user
@router.put("/users/{user_id}", response_model=schemas.UserShow)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,  # Fix: Change UserCreate to UserUpdate
    db: Session = Depends(get_db),
    current_user: schemas.UserShow = Depends(auth.get_current_user),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user=user, user_id=user_id)


# delete a user
@router.delete("/users/{user_id}", response_model=schemas.UserShow)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserShow = Depends(auth.get_current_user),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


# get a user's preferences
@router.get("/preferences/{user_id}", response_model=schemas.UserPreferences)
def read_user_preferences(user_id: int, db: Session = Depends(get_db)):
    db_preferences = crud.get_user_preferences(db, user_id=user_id)
    if db_preferences is None:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return db_preferences
