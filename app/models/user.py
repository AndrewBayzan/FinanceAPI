from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True
    )


