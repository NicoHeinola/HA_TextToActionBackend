from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chat_history",
        sa.Column("id", sa.Integer, primary_key=True),
    )


def downgrade():
    op.drop_table("chat_history")
