#!/usr/bin/env python3


"""Module to hold routes related to users"""

from typing import Generator, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import auth
from database import get_db

router = APIRouter()


# create a user
@router.post("/register", response_model=schemas.UserShow)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (schemas.UserCreate): The user data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.UserShow: The created user.

    Examples:
        Example usage to create a new user:
        ```python
        {
            "email": "",
            "phone": "1234567890",
            "password": "test"
        }
        ```

    Raises:
        HTTPException: If the user's credentials (email or phone) are already registered.

    """
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
    """
    Get all users.

    Args:
        skip (int, optional): Number of users to skip. Defaults to 0.
        limit (int, optional): Maximum number of users to retrieve. Defaults to 100.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (schemas.UserShow, optional): The current user. Defaults to Depends(auth.get_current_user).

    Returns:
        List[schemas.UserShow]: List of users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# get a user by their id
@router.get("/users/{user_id}", response_model=schemas.UserShow)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserShow = Depends(auth.get_current_user),
):
    """
    Get a user by their ID.

    Args:
        user_id (int): The ID of the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (schemas.UserShow, optional): The current user. Defaults to Depends(auth.get_current_user).

    Returns:
        schemas.UserShow: The user.

    Raises:
        HTTPException: If the user is not found.

    Examples:
        Example usage to get a user by their ID:
        ```python
        {
            "id": 1
        }
        ```
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# update a user
@router.put("/users/{user_id}", response_model=schemas.UserShow)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,  # Fix: Change UserCreate to UserUpdate
    db: Session = Depends(get_db),
    current_user: schemas.UserShow = Depends(auth.get_current_user),
):
    """
    Update a user.

    Args:
        user_id (int): The ID of the user to update.
        user (schemas.UserUpdate): The updated user data.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (schemas.UserShow, optional): The current user. Defaults to Depends(auth.get_current_user).

    Returns:
        schemas.UserShow: The updated user.

    Raises:
        HTTPException: If the user is not found in the database.

    Examples:
        Example usage to update a user:
        ```python
        {
            "email": "",
            "phone": "1234567890",
            "password": "test"
        }
        ```
    """
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
    """
    Delete a user.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (schemas.UserShow, optional): The current user. Defaults to Depends(auth.get_current_user).

    Returns:
        schemas.UserShow: The deleted user.

    Raises:
        HTTPException: If the user is not found in the database.

    Examples:
        Example usage to delete a user:
        ```python
        {
            "id": 1
        }
        ```
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


# get a user's preferences
@router.get("/preferences/{user_id}", response_model=schemas.UserPreferences)
def read_user_preferences(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user's preferences.

    Args:
        user_id (int): The ID of the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.UserPreferences: The user's preferences.
    """
    db_preferences = crud.get_user_preferences(db, user_id=user_id)
    if db_preferences is None:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return db_preferences
