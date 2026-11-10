from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.users import User
from app.core.security import hash_password
from app.schemas.user import UserCreate
from app.exceptions.user import UsernameAlreadyExistsError, EmailAlreadyExistsError


def create_user(
        db: Session,
        user_data: UserCreate
        ):
    existing_user = db.scalar(
        select(User).where(User.username == user_data.username)
    )
    if existing_user:
        raise UsernameAlreadyExistsError("Username already registered")

    existing_email = db.scalar(
        select(User).where(User.email == user_data.email)
    )
    if existing_email:
        raise EmailAlreadyExistsError("Email already registered")

    hashed_password = hash_password(user_data.password.get_secret_value())

    user = User(
        username=user_data.username,
        password_hash=hashed_password,
        email=user_data.email)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as error:
        db.rollback()

        constraint_name = error.orig.diag.constraint_name

        if constraint_name == "uq_users_username":
            raise UsernameAlreadyExistsError() from error

        if constraint_name == "uq_users_email":
            raise EmailAlreadyExistsError() from error

        raise
    return user