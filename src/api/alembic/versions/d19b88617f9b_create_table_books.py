"""create_table_books

Revision ID: d19b88617f9b
Revises: 7f00b3aa7fe5
Create Date: 2023-06-29 14:57:51.742991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd19b88617f9b'
down_revision = '7f00b3aa7fe5'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
        "books",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("pages", sa.BigInteger, nullable=False),
        sa.Column("author_id", sa.Integer, nullable=False),
    )


def downgrade():
  op.drop_table("books")
