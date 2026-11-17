from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import jwt

from app.models.refresh_token import RefreshToken
from app.core.security import create_refresh_token, decode_access_token

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

    
