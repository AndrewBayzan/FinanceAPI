from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db

from app.core.config import settings
from app.db.base import Base
from app import models


test_engine = create_engine(settings.test_db_url)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    expire_on_commit=False
)

@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_db, None)

@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(test_engine)

@pytest.fixture
def db(create_test_tables):
    connection = test_engine.connect()
    transaction = connection.begin()

    db = TestSessionLocal(
        bind=connection,
        join_transaction_mode="create_savepoint"
    )

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()