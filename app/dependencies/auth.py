from fastapi import Depends, HTTPException, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
import jwt

from app.dependencies.database import get_db
from app.core.security import decode_access_token
from app.models.users import User


def get_current_user(access_token: str | None = Cookie(default=None), db: Session = Depends(get_db)) -> User:
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = decode_access_token(access_token)
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid aaccess token")
    
    user = db.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
