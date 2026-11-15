from datetime import timedelta, datetime, timezone
from pwdlib import PasswordHash
import jwt
import secrets

from app.core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(
        password: str,
        hash_password: str
        ) -> bool:
    return password_hash.verify(password, hash_password)
    
def create_access_token(user_id: int) -> str:
    iat = datetime.now(timezone.utc)
    exp = iat + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "iat": iat,
        "exp": exp
    }
    access_token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    return access_token

def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm]
    )

    return payload

def create_refresh_token(user_id: int) -> str:
    refresh_token = secrets.token_urlsafe(64)