"""Initial migration.

Revision ID: b6dab5e5cdac
Revises: None
Create Date: 2020-03-15 16:18:16.152717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b6dab5e5cdac"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "todo_item",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("msg", sa.String(length=100), nullable=False),
        sa.Column("is_done", sa.Boolean(), nullable=False),
        sa.CheckConstraint(
            "length(msg) >= 1 AND length(msg) <= 50",
            name=op.f("ck_todo_item_msg_length"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_todo_item")),
    )


def downgrade():
    op.drop_table("todo_item")
