from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserResponse, UserCreate
from app.services.register_service import create_user
from app.exceptions.user import UsernameAlreadyExistsError, EmailAlreadyExistsError

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
            "/register",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED
             )
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        user = create_user(db=db, user_data=user_data)
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

    return user