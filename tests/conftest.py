from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.core.config import settings
from app.db.base import Base
import app.models


test_engine = create_engine(settings.test_db_url)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    expire_on_commit=False
)

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