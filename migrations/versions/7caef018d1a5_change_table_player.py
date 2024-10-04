"""change table player

Revision ID: 7caef018d1a5
Revises: 6f21cd380a34
Create Date: 2024-10-04 13:21:26.456216

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7caef018d1a5"
down_revision: Union[str, None] = "6f21cd380a34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("player", sa.Column("id_role", sa.Integer(), nullable=False))
    op.drop_constraint("player_uc", "player", type_="unique")
    op.create_unique_constraint(
        "player_uc",
        "player",
        ["first_name", "last_name", "patronymic", "id_role"],
    )
    op.drop_constraint("player_role_fkey", "player", type_="foreignkey")
    op.create_foreign_key(
        None, "player", "role", ["id_role"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("player", "role")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "player",
        sa.Column("role", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "player", type_="foreignkey")
    op.create_foreign_key(
        "player_role_fkey",
        "player",
        "role",
        ["role"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint("player_uc", "player", type_="unique")
    op.create_unique_constraint(
        "player_uc",
        "player",
        ["first_name", "last_name", "patronymic", "role"],
    )
    op.drop_column("player", "id_role")
    # ### end Alembic commands ###
