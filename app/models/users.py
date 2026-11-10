from datetime import datetime
from sqlalchemy import String, func, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
    UniqueConstraint("username", name="uq_users_username"),
    UniqueConstraint("email", name="uq_users_email"),
    )

