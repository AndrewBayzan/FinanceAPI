from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey, CheckConstraint, Enum, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.enums.transaction import TransactionType

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(
        TransactionType,
        values_callable=lambda enum_cls: [member.value for member in enum_cls]
        ),
        nullable=False
        )
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    transaction_date: Mapped[date] = mapped_column(server_default=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.current_date(), nullable=False)

    __table_args__ = (
        CheckConstraint("amount > 0.00", name="chk_amount"),
    )