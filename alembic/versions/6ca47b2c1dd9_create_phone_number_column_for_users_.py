"""create phone number column for users table

Revision ID: 6ca47b2c1dd9
Revises: 
Create Date: 2024-04-20 19:30:43.796981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ca47b2c1dd9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.Integer(),nullable=True))


def downgrade() -> None:
    pass
