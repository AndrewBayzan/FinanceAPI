from fastapi import Depends, HTTPException, Cookie, status
from sqlalchemy.orm import Session
from sqlalchemy import select
import jwt

from app.dependenсies.database import get_db
from app.core.security import decode_access_token
from app.models.users import User

def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    try:
        decoded_token = decode_access_token(token)
        user_id = int(decoded_token["sub"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401)
    
    user = db.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
