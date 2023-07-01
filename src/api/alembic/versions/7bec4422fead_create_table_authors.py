"""create_table_authors

Revision ID: 7bec4422fead
Revises: d19b88617f9b
Create Date: 2023-06-30 08:48:01.692643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bec4422fead'
down_revision = 'd19b88617f9b'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
      "authors",
      sa.Column("id", sa.Integer, primary_key=True),
      sa.Column("name", sa.String(100), nullable=False),
  )


def downgrade():
  op.drop_table("authors")
