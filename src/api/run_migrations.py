from alembic import command
from alembic.config import Config

# Load the Alembic configuration
alembic_cfg = Config("alembic.ini")

# Run the migrations
command.upgrade(alembic_cfg, "head")