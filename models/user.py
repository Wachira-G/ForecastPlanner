#!/usr/bin/env python3


"""Module for user functionality."""

from passlib.context import CryptContext

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import relationship
from database import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """Create and verify password hashes."""

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        """Compare a password and a hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        """Make a hash of a password."""
        return pwd_context.hash(password)


class User(Base):
    """Define the functionality of a user of our app."""

    __tablename__ = "users"

    user_id = Column(
        Integer, primary_key=True, autoincrement=True, server_default=text("1")
    )
    email = Column(String(255), nullable=True, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    gender = Column(Enum("female", "male", "other", name="gender_enum", schema='public', create_type=False))


class User_Preferences(Base):
    """Define a users preferrences."""

    __tablename__ = "user_preferences"

    preference_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    preferred_units = Column(
        Enum("Celcius", "Fahrenheit", name="preferred_units_enum")
    )  # (e.g., Celsius or Fahrenheit)
    favorite_locations = Column(Text)
    notification_settings = Column(Boolean)
