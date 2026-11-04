from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime, Date, ForeignKey, ForeignKeyConstraint, CheckConstraint, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.enums.transaction import TransactionType

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(
        TransactionType,
        values_callable=lambda enum_cls: [member.value for member in enum_cls]
        ),
        nullable=False
        )
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    transaction_date: Mapped[date] = mapped_column(Date, server_default=func.current_date(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("amount > 0.00", name="chk_amount"),
        ForeignKeyConstraint(
            ["user_id", "account_id"],
            ["accounts.user_id", "accounts.id"],
            name="fk_transaction_account"
            )
    )