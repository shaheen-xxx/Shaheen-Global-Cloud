"""Dependency injection"""

from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.base import get_db as _get_db
from app.core.security import decode_token
from app.database.models import User


async def get_db() -> Session:
    """Get database session"""
    async for db in _get_db():
        yield db


async def get_current_user(db: Session = Depends(get_db)) -> User:
    """Get current authenticated user"""
    # For MVP, we'll use a mock user
    user = db.query(User).filter(User.username == "testuser").first()
    if not user:
        # Create test user if it doesn't exist
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="$2b$12$fake_hash"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
