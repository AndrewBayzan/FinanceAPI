from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Numeric, Date, DateTime, ForeignKey, CheckConstraint, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.enums.transfer import CommissionSource


class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    source_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    destination_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    transfer_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    commission: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False, default=Decimal("0.00"))
    commission_source: Mapped[CommissionSource | None] = mapped_column(Enum(CommissionSource, values_callable=lambda enum_cls: [ member.value for member in enum_cls]), nullable=True)
    transfer_date: Mapped[date] = mapped_column(Date, server_default=func.current_date(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("transfer_amount > 0.00", name="chk_transfer_amount"),
        CheckConstraint("commission >= 0.00", name="chk_commission"),
        CheckConstraint("source_account_id != destination_account_id", name="chk_different_accounts"),
        CheckConstraint("(commission = 0 AND commission_source IS NULL) OR " \
                        "(commission > 0 AND commission_source IS NOT NULL)",
                        name="chk_commission_source"
                        ),
    )