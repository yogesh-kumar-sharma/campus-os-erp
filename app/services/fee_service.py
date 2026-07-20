from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.fee import FeeCategory, Payment, StudentFee
from app.schemas.fee import FeeCategoryCreate, PaymentCreate, StudentFeeCreate
class FeeError(Exception): pass
class FeeService:
    def __init__(self, session: AsyncSession): self.session = session
    async def category(self, payload: FeeCategoryCreate) -> FeeCategory:
        item = FeeCategory(**payload.model_dump()); self.session.add(item); await self.session.commit(); return item
    async def assign(self, payload: StudentFeeCreate) -> StudentFee:
        item = StudentFee(**payload.model_dump()); self.session.add(item); await self.session.commit(); return item
    async def pay(self, fee_id: UUID, payload: PaymentCreate) -> Payment:
        fee = await self.session.get(StudentFee, fee_id)
        if fee is None: raise FeeError("Fee record not found")
        paid = (await self.session.execute(select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.student_fee_id == fee_id))).scalar_one()
        if paid + payload.amount > fee.amount_due: raise FeeError("Payment exceeds pending amount")
        item = Payment(student_fee_id=fee_id, receipt_number=f"RCP-{uuid4().hex[:12].upper()}", **payload.model_dump())
        self.session.add(item); await self.session.commit(); return item
    async def status(self, student_id: UUID) -> list[dict]:
        fees = list((await self.session.execute(select(StudentFee).where(StudentFee.student_id == student_id))).scalars())
        rows=[]
        for fee in fees:
            paid=(await self.session.execute(select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.student_fee_id == fee.id))).scalar_one()
            rows.append({"fee_id":fee.id,"amount_due":fee.amount_due,"amount_paid":paid,"pending_amount":fee.amount_due-paid})
        return rows
