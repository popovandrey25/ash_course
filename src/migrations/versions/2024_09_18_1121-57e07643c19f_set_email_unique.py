"""set email=unique

Revision ID: 57e07643c19f
Revises: 5c50d2fe7862
Create Date: 2024-09-18 11:21:50.369535

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "57e07643c19f"
down_revision: Union[str, None] = "5c50d2fe7862"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
