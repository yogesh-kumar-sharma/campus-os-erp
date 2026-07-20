"""create notices
Revision ID: 0010_notices
Revises: 0009_fees
"""
from typing import Sequence,Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
revision: str="0010_notices"
down_revision: Union[str,None]="0009_fees"
branch_labels: Union[str,Sequence[str],None]=None
depends_on: Union[str,Sequence[str],None]=None
def upgrade()->None:
 op.create_table("notices",sa.Column("title",sa.String(200),nullable=False),sa.Column("content",sa.Text(),nullable=False),sa.Column("audience",sa.String(20),nullable=False),sa.Column("created_by_id",postgresql.UUID(as_uuid=True),nullable=False),sa.Column("is_active",sa.Boolean(),nullable=False),sa.Column("id",postgresql.UUID(as_uuid=True),nullable=False),sa.PrimaryKeyConstraint("id"))
def downgrade()->None:op.drop_table("notices")
