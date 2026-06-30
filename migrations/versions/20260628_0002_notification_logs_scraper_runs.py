"""notification logs and scraper runs

Revision ID: 20260628_0002
Revises: 20260628_0001
Create Date: 2026-06-28 21:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260628_0002"
down_revision: Union[str, Sequence[str], None] = "20260628_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return table_name in inspector.get_table_names()


def upgrade() -> None:
    if not _table_exists("notification_logs"):
        op.create_table(
            "notification_logs",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("user_oferta_id", sa.Integer(), nullable=True),
            sa.Column("channel_id", sa.Integer(), nullable=True),
            sa.Column("channel_type", sa.String(), nullable=False),
            sa.Column("destination", sa.String(), nullable=False),
            sa.Column("status", sa.String(), nullable=False),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("sent_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["channel_id"], ["notification_channels.id"]),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.ForeignKeyConstraint(["user_oferta_id"], ["user_ofertas.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_notification_logs_id"), "notification_logs", ["id"], unique=False)
        op.create_index(op.f("ix_notification_logs_user_id"), "notification_logs", ["user_id"], unique=False)
        op.create_index(op.f("ix_notification_logs_user_oferta_id"), "notification_logs", ["user_oferta_id"], unique=False)
        op.create_index(op.f("ix_notification_logs_channel_id"), "notification_logs", ["channel_id"], unique=False)

    if not _table_exists("scraper_runs"):
        op.create_table(
            "scraper_runs",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("query", sa.String(), nullable=False),
            sa.Column("status", sa.String(), nullable=False),
            sa.Column("started_at", sa.DateTime(), nullable=True),
            sa.Column("finished_at", sa.DateTime(), nullable=True),
            sa.Column("offers_found", sa.Integer(), nullable=True),
            sa.Column("new_offers", sa.Integer(), nullable=True),
            sa.Column("new_matches", sa.Integer(), nullable=True),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_scraper_runs_id"), "scraper_runs", ["id"], unique=False)


def downgrade() -> None:
    if _table_exists("scraper_runs"):
        op.drop_table("scraper_runs")
    if _table_exists("notification_logs"):
        op.drop_table("notification_logs")
