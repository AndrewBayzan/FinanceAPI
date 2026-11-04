from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, CheckConstraint, ForeignKey, UniqueConstraint, text, func
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    currency: Mapped[str] = mapped_column(String(5), server_default=text("'RUB'"), nullable=False)
    initial_balance: Mapped[Decimal] = mapped_column(Numeric(10,2), server_default=text("0.00"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_account"),
        UniqueConstraint("user_id", "id", name="uq_account_user_id"),
        CheckConstraint("initial_balance >= 0", name="chk_init_balance" ),
    )