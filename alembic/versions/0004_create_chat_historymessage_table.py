from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chat_history_message",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("chat_history_id", sa.Integer, nullable=False),
        sa.Column("message", sa.Text, nullable=True, index=True),
        sa.Column("type", sa.String, nullable=True),  # e.g., 'user' or 'AI'
        sa.ForeignKeyConstraint(["chat_history_id"], ["chat_history.id"], ondelete="CASCADE"),
    )


def downgrade():
    op.drop_table("chat_history_message")
