from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import jwt

from app.models.refresh_token import RefreshToken
from app.core.security import create_access_token, create_refresh_token
from app.models.users import User

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