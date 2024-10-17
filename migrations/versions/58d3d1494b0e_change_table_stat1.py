"""change table Stat1

Revision ID: 58d3d1494b0e
Revises: 96cc8fac3f24
Create Date: 2024-10-08 14:50:10.742080

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "58d3d1494b0e"
down_revision: Union[str, None] = "96cc8fac3f24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "stat", "id_assistant", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "stat", "id_assistant", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###