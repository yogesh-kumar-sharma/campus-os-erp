"""create documents
Revision ID: 0011_documents
Revises: 0010_notices
"""
from typing import Sequence,Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
revision: str="0011_documents";down_revision: Union[str,None]="0010_notices";branch_labels: Union[str,Sequence[str],None]=None;depends_on: Union[str,Sequence[str],None]=None
def upgrade()->None:op.create_table("documents",sa.Column("owner_user_id",postgresql.UUID(as_uuid=True),nullable=False),sa.Column("document_type",sa.String(80),nullable=False),sa.Column("storage_path",sa.String(500),nullable=False),sa.Column("content_type",sa.String(100),nullable=False),sa.Column("id",postgresql.UUID(as_uuid=True),nullable=False),sa.PrimaryKeyConstraint("id"))
def downgrade()->None:op.drop_table("documents")
