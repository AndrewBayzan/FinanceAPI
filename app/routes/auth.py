from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserLogin, AuthResponse, TokenResponse, RefreshRequest
from app.services.auth import auth_user, issue_tokens, refresh_tokens
from app.exceptions.user import InvalidEmailOrPassword
from app.exceptions.token import InvalidRefreshToken

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/", response_model=AuthResponse)
def login(user_data:UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = auth_user(db, user_data.email, user_data.password.get_secret_value())
    except InvalidEmailOrPassword:
        raise HTTPException(status_code=401 ,detail="Invalid Email or Password")
    
    tokens = issue_tokens(db, user)

    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        samesite="lax",
        max_age=900
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        samesite="lax",
        max_age=604_800
    )
    
    return {
        "user": user
        }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
    )
    response.delete_cookie(
        key="refresh_token",
    )


@router.post("/refresh", status_code=status.HTTP_200_OK )
def refresh(
            response: Response,
            refresh_token: str | None = Cookie(default=None),
            db: Session = Depends(get_db)
            ):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    try:
        tokens = refresh_tokens(db, refresh_token)
    except InvalidRefreshToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    response.set_cookie(
        key="access_token",
        value= tokens["access_token"],
        httponly=True,
        samesite="lax",
        max_age=900
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        samesite="lax",
        max_age=604_800
    )

    return {"message": "tokens refreshed"}