"""TodoItem relationship with User.

Revision ID: 64f9e3f72798
Revises: 5c48022e325d
Create Date: 2020-04-21 21:50:55.662077

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "64f9e3f72798"
down_revision = "5c48022e325d"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("todo_item", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        op.f("fk_todo_item_user_id_user"), "todo_item", "user", ["user_id"], ["id"]
    )


def downgrade():
    op.drop_constraint(
        op.f("fk_todo_item_user_id_user"), "todo_item", type_="foreignkey"
    )
    op.drop_column("todo_item", "user_id")
