from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from datetime import timezone, datetime
import hashlib
import jwt

from app.models.refresh_token import RefreshToken
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.models.users import User
from app.exceptions.user import InvalidEmailOrPassword
from app.exceptions.token import InvalidRefreshToken
from app.schemas.user import RefreshRequest

def save_refresh_token(db: Session, user_id: int) -> str:
    token = create_refresh_token(user_id)
    saved_token = RefreshToken(
        user_id=user_id, 
        token_hash=token["token_hash"], 
        expires_at=token["expires_at"]
        )

    try:
        db.add(saved_token)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    return token["refresh_token"]

def issue_tokens(db: Session, user: User) -> dict:
    access_token = create_access_token(user.id)
    refresh_token = save_refresh_token(db, user.id)

    return {
        "access_token" : access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def auth_user(db: Session, email:  str, password: str) -> User:
    user = db.scalars(select(User).where(User.email == email)).first()

    if not user:
        raise InvalidEmailOrPassword

    checked_password = verify_password(password, user.password_hash)
    if not checked_password:
        raise InvalidEmailOrPassword

    return user

def refresh_tokens(db: Session, data: RefreshRequest) -> dict:
    hashed_token = hashlib.sha256(data.refresh_token.encode()).hexdigest()
    refresh_token = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hashed_token))
    
    if not refresh_token:
        raise InvalidRefreshToken

    if refresh_token.revoked_at is not None:
        raise InvalidRefreshToken
    elif refresh_token.expires_at <= datetime.now(timezone.utc):
        raise InvalidRefreshToken
    else:
        refresh_token.revoked_at = datetime.now(timezone.utc)
        access_token = create_access_token(refresh_token.user_id)
        new_refresh_token = create_refresh_token(refresh_token.user_id)
        saved_token = RefreshToken(
            user_id=refresh_token.user_id,
            token_hash=new_refresh_token["token_hash"],
            expires_at=new_refresh_token["expires_at"]
            )
        try:
            db.add(saved_token)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token["refresh_token"],
        }
