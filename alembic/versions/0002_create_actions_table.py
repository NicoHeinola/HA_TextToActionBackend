from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "actions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=True, index=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("meta", sa.JSON, nullable=True, default={}),
    )


def downgrade():
    op.drop_table("actions")
