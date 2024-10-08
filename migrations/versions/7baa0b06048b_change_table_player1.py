"""change table player1

Revision ID: 7baa0b06048b
Revises: 7caef018d1a5
Create Date: 2024-10-04 13:35:16.165678

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7baa0b06048b"
down_revision: Union[str, None] = "7caef018d1a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "player",
        "id_role",
        existing_type=sa.INTEGER(),
        server_default=None,
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "player",
        "id_role",
        existing_type=sa.INTEGER(),
        server_default=sa.text("4"),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
