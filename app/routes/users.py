from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.user_service import get_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def read_users(db: Annotated[Session, Depends(get_db)]):
    users = get_users(db)

    return users