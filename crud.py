#!/usr/bin/env python3

"""Module to created crud operations for our app."""

from sqlalchemy.orm import Session

import models
import schemas
from models.user import Hasher


def get_user(db: Session, user_id: int) -> models.user.User:
    """
    Retrieve a user from the database based on the user_id.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user object if found, None otherwise.
    """
    return (
        db.query(models.user.User).filter(
            models.user.User.user_id == user_id).first()
    )


def get_user_by_email(db: Session, email: str) -> models.user.User:
    """
    Retrieve a user from the database based on their email.

    Args:
        db (Session): The database session.
        email (str): The email of the user to retrieve.

    Returns:
        models.user.User: The user object retrieved from the database.
    """
    return db.query(models.user.User).filter(
        models.user.User.email == email).first()


def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[models.user.User]:
    """
    Retrieve a list of users from the database.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to retrieve.
          Defaults to 100.

    Returns:
        list[models.user.User]: A list of user objects.
    """
    return db.query(models.user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.user.User:
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to be created.

    Returns:
        User: The created user object.
    """
    db_user = models.user.User(
        email=user.email, password=Hasher.get_password_hash(user.password)
    )
    for attribute, value in user.model_dump().items():
        if (
            attribute != "password"
            and attribute != "email"
            and hasattr(db_user, attribute)
        ):
            setattr(db_user, attribute, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, user: schemas.UserUpdate, user_id: int
) -> models.user.User:
    """
    Update a user in the database.

    Args:
        db (Session): The database session.
        user (schemas.UserUpdate): The updated user data.
        user_id (int): The ID of the user to be updated.

    Returns:
        schemas.User: The updated user object.
    """
    db_user = get_user(db, user_id)

    if user.email and user.email != db_user.email:
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            raise ValueError("Email already exists")
        db_user.email = user.email

    if user.password:
        db_user.password = Hasher.get_password_hash(user.password)

    for attribute, value in user.dict(exclude_unset=True).items():
        if attribute not in ["email", "password"] and hasattr(db_user, attribute):
            setattr(db_user, attribute, value)

    db.commit()
    db.refresh(db_user)
    return db_user


"""
def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    # TODO: the UserCreate makes it a must that we supply
    # a username and password for us to update, must we do this?
    db_user = get_user(db, user_id)
    if user.email and user.email != db_user.email:
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            raise ValueError("Email already exists")
        db_user.email = user.email
    else:
        user.email = db_user.email
    if user.password and user.password != db_user.password:
        db_user.password = Hasher.get_password_hash(user.password)
    else:
        user.password = db_user.password
    for attribute, value in user.model_dump().items():
        if attribute != "password" and attribute != "email" and hasattr(db_user, attribute):
            setattr(db_user, attribute, value)
    db.commit()
    db.refresh(db_user)
    return db_user
"""


def delete_user(db: Session, user_id: int) -> dict:
    """
    Deletes a user from the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to be deleted.

    Returns:
        dict: An empty dictionary indicating the deletion was successful.
    """
    db_user = (
        db.query(models.user.User).filter(models.user.User.user_id == user_id).first()
    )
    db.delete(db_user)
    db.commit()
    return {}


def get_user_preferences(db: Session, user_id: int) -> models.user.User_Preferences:
    """
    Retrieve the user preferences from the database based on the user ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        models.user.User_Preferences: The user preferences.

    """
    return (
        db.query(models.user.User_Preferences)
        .filter(models.user.User_Preferences.user_id == user_id)
        .first()
    )
