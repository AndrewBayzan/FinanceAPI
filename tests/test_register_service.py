from app.services.register_service import create_user
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password
from app.core.security import hash_password
from app.models.users import User
from app.exceptions.user import UsernameAlreadyExistsError, EmailAlreadyExistsError
import pytest

from sqlalchemy import select

def test_create_user(db):
    user_data = UserCreate(
        username="testuser",
        email="test@mail.com",
        password="1111"
    )

    create_user(db, user_data)
    user = db.scalar(select(User).where(User.username == user_data.username))
    assert user is not None

def test_correct_credential(db):
    user_data = UserCreate(
            username="testuser",
            email="test@mail.com",
            password="1111"
        )

    create_user(db, user_data)

    query = db.scalar(select(User).where(User.username == user_data.username))

    assert query.username == user_data.username
    assert query.email == user_data.email
    assert query.password_hash != user_data.password.get_secret_value()   


def test_username_already_exists(db):
    user_data = UserCreate(
        username="testuser",
        email="test@mail.com",
        password="1111"
    )

    user1 = create_user(db, user_data)

    with pytest.raises(UsernameAlreadyExistsError):
        user2 = create_user(db, user_data)

def test_email_already_exists(db):
    user_data1 = UserCreate(
        username="testuser",
        email="test@mail.com",
        password="1111"
    )
    user_data2 = UserCreate(
        username="testuser2",
        email="test@mail.com",
        password="1111"
    )

    user1 = create_user(db, user_data1)

    with pytest.raises(EmailAlreadyExistsError):
        user2 = create_user(db, user_data2)

def test_create_user_password_hash(db):
    user_data = UserCreate(
        username="testuser",
        email="test@mail.com",
        password="1111"
    )

    create_user(db, user_data)
    user = db.scalar(select(User).where(User.username == user_data.username))

    hashed = verify_password(user_data.password.get_secret_value(), user.password_hash)

    assert hashed is True
   