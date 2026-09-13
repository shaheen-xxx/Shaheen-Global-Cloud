"""Test configuration and fixtures"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
from app.main import app
from fastapi.testclient import TestClient

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEM_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    """Database fixture"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)
