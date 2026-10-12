"""Initial scenario and run tables.

Revision ID: 0001
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('scenarios',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('level', sa.String(length=20), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table('plan_runs',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('scenario_id', sa.String(length=36), sa.ForeignKey('scenarios.id'), nullable=False),
        sa.Column('engine', sa.String(length=50), nullable=False),
        sa.Column('result', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_runs_scenario', 'plan_runs', ['scenario_id'])

def downgrade():
    op.drop_index('ix_runs_scenario', table_name='plan_runs')
    op.drop_table('plan_runs')
    op.drop_table('scenarios')
