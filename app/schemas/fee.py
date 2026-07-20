from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
class FeeCategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    default_amount: Decimal = Field(gt=0)
class StudentFeeCreate(BaseModel):
    student_id: UUID
    fee_category_id: UUID
    amount_due: Decimal = Field(gt=0)
    due_date: date
class PaymentCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    paid_on: date
    payment_method: str = Field(min_length=2, max_length=30)
class FeeStatus(BaseModel):
    fee_id: UUID
    amount_due: Decimal
    amount_paid: Decimal
    pending_amount: Decimal
