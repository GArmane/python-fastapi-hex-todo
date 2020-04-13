"""Create user table.

Revision ID: 5c48022e325d
Revises: b6dab5e5cdac
Create Date: 2020-04-13 00:02:25.343492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5c48022e325d"
down_revision = "b6dab5e5cdac"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("email", name=op.f("uq_user_email")),
    )


def downgrade():
    op.drop_table("user")
