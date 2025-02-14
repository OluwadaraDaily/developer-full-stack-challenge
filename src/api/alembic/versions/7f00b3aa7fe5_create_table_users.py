"""create_table_users

Revision ID: 7f00b3aa7fe5
Revises: 
Create Date: 2023-06-29 12:34:04.385729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f00b3aa7fe5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    "users",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String(100), unique=True, nullable=False),
    sa.Column("password", sa.LargeBinary, nullable=False),
  )


def downgrade():
  op.drop_table("users")
