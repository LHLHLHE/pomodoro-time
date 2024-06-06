"""category type

Revision ID: 59821c2d2b31
Revises: 18f52eaf2ebf
Create Date: 2024-05-29 20:25:49.556752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59821c2d2b31'
down_revision: Union[str, None] = '18f52eaf2ebf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'type')
    # ### end Alembic commands ###
