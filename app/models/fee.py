"""Fee categories, student liabilities, and payment history."""
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

class FeeCategory(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "fee_categories"
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    default_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

class StudentFee(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "fees"
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id"), nullable=False)
    fee_category_id: Mapped[UUID] = mapped_column(ForeignKey("fee_categories.id"), nullable=False)
    amount_due: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)

class Payment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "payments"
    student_fee_id: Mapped[UUID] = mapped_column(ForeignKey("fees.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    paid_on: Mapped[date] = mapped_column(Date, nullable=False)
    receipt_number: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), nullable=False)
