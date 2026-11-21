from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserLogin, AuthResponse
from app.services.auth import auth_user, issue_tokens
from app.exceptions.user import InvalidEmailOrPassword

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/", response_model=AuthResponse)
def login(user_data:UserLogin, db: Session = Depends(get_db)):
    try:
        user = auth_user(db, user_data.email, user_data.password.get_secret_value())
    except InvalidEmailOrPassword:
        raise HTTPException(status_code=401 ,detail="Invalid Email or Password")
    
    tokens = issue_tokens(db, user)
    return {
        "user": user,
        **tokens
        }

