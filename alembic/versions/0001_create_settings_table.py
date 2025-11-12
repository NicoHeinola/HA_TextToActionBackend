from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "settings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("key", sa.String, nullable=False, unique=True, index=True),
        sa.Column("value", sa.String, nullable=False),
        sa.Column("type", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("settings")
