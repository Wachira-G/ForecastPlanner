#!/usr/bin/env python3

"""Module to hold the token blocklist model."""

from datetime import datetime
from fastapi import Depends
from jose import jwt
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session

import database
from config import settings


class TokenBlocklist(database.Base):
    """Implement a token blocklist model.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "token_blocklist"

    id = Column(Integer, autoincrement=True, primary_key=True)
    jti = Column(String(255))
    token_type = Column(String)
    exp = Column(DateTime)

    def save(self, db: Session):
        """Save a block list model."""
        db.add(self)
        db.commit()

    @classmethod
    def save_from_token(cls, token, db: Session):
        """Save a block list model from a supplied token string."""
        token_dict = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        jti = token_dict.get("jti")
        token_type = "bearer"  # can we get a way to populate this
        exp = datetime.fromtimestamp(token_dict.get("exp", 0))
        blocklist_token = cls(jti=jti, token_type=token_type, exp=exp)
        blocklist_token.save(db)

    @classmethod
    def is_jti_blocklisted(cls, jti, db: Session):
        """Check if a token is blocklisted."""
        query = db.query(cls).filter_by(jti=jti).first()
        return bool(query)

    @staticmethod
    def clean_block_list(db: Session = Depends(database.get_db)):
        """Delete all block list entries."""
        now = datetime.now()
        blocklisted_tokens = db.query(TokenBlocklist).all()
        for token in blocklisted_tokens:
            if token.exp <= now:
                db.delete(token)
        db.commit()
