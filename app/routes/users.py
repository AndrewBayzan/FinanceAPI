from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserResponse, UserCreate, AuthResponse
from app.services.register_service import create_user
from app.exceptions.user import UsernameAlreadyExistsError, EmailAlreadyExistsError
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.services.auth import issue_tokens

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
            "/register",
             response_model=AuthResponse,
             status_code=status.HTTP_201_CREATED
             )
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        user = create_user(db=db, user_data=user_data)
        tokens = issue_tokens(db, user)
    except UsernameAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Username already registered"
            )

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return {"user": user,
             **tokens
            }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user