"""create fees
Revision ID: 0009_fees
Revises: 0008_examinations
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
revision: str="0009_fees"
down_revision: Union[str,None]="0008_examinations"
branch_labels: Union[str,Sequence[str],None]=None
depends_on: Union[str,Sequence[str],None]=None
def upgrade()->None:
 op.create_table("fee_categories",sa.Column("name",sa.String(100),nullable=False),sa.Column("default_amount",sa.Numeric(12,2),nullable=False),sa.Column("id",postgresql.UUID(as_uuid=True),nullable=False),sa.PrimaryKeyConstraint("id"),sa.UniqueConstraint("name"))
 op.create_table("fees",sa.Column("student_id",postgresql.UUID(as_uuid=True),nullable=False),sa.Column("fee_category_id",postgresql.UUID(as_uuid=True),nullable=False),sa.Column("amount_due",sa.Numeric(12,2),nullable=False),sa.Column("due_date",sa.Date(),nullable=False),sa.Column("id",postgresql.UUID(as_uuid=True),nullable=False),sa.PrimaryKeyConstraint("id"))
 op.create_table("payments",sa.Column("student_fee_id",postgresql.UUID(as_uuid=True),nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("paid_on",sa.Date(),nullable=False),sa.Column("receipt_number",sa.String(80),nullable=False),sa.Column("payment_method",sa.String(30),nullable=False),sa.Column("id",postgresql.UUID(as_uuid=True),nullable=False),sa.PrimaryKeyConstraint("id"),sa.UniqueConstraint("receipt_number"))
def downgrade()->None: op.drop_table("payments");op.drop_table("fees");op.drop_table("fee_categories")
