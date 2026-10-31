from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users import User
from app.db.session import get_db

def get_users(db: Session):
    stmt = select(User)
    users = db.scalars(stmt).all()
    
    return users