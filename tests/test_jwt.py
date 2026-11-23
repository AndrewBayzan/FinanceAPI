import pytest
import jwt
from datetime import datetime, timezone, timedelta
from app.core.config import settings

from app.core.security import create_access_token, decode_access_token

def test_create_access_token():
    token = create_access_token(1)
    payload = decode_access_token(token)

    assert payload["sub"] == "1"

def test_access_token_has_exp():
    token = create_access_token(1)
    payload = decode_access_token(token)

    assert "exp" in payload
    assert payload["exp"] > datetime.now(timezone.utc).timestamp()

def test_fake_token():
    iat = datetime.now(timezone.utc)
    exp = iat + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(1),
        "iat": iat,
        "exp": exp
    }
    access_token = jwt.encode(payload, "fake_secret", algorithm=settings.jwt_algorithm)

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(access_token)

def test_expired_token():
    iat = datetime.now(timezone.utc)
    exp = iat - timedelta(seconds=1)
    payload = {
        "sub": str(1),
        "iat": iat,
        "exp": exp
    }
    access_token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(access_token)

def test_token_without_sub():
    iat = datetime.now(timezone.utc)
    exp = iat + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "iat": iat,
        "exp": exp
    }
    access_token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    decoded_token = decode_access_token(access_token)

    with pytest.raises(KeyError):
        decoded_token["sub"]

