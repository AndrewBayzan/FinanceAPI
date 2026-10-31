from datetime import datetime
from sqlalchemy import String, ForeignKey, Enum, func, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.enums.transaction import TransactionType

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(
        TransactionType,
        values_callable=lambda enum_cls: [member.value for member in enum_cls]
        ), 
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("uq_sys_categories_name_type", 
              "name", 
              "type", 
              postgresql_where=text("user_id IS NULL"),
              unique=True),
        Index("uq_user_categories_name_type",
              "user_id",
              "name",
              "type",
              postgresql_where=text("user_id IS NOT NULL"),
              unique=True
              )

    )