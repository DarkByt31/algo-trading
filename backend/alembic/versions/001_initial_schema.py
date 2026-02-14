"""Initial schema with all tables

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-02-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create algorithms table
    op.create_table(
        'algorithms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create backtest_jobs table
    op.create_table(
        'backtest_jobs',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('algorithm_id', sa.String(50), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('initial_capital', sa.Numeric(12, 2), nullable=False),
        sa.Column('allow_short', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('brokerage_fee', sa.Numeric(8, 2), nullable=True, server_default='20'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='queued'),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('execution_time_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    # Create backtest_results table
    op.create_table(
        'backtest_results',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('job_id', sa.String(36), nullable=False),
        sa.Column('final_capital', sa.Numeric(12, 2), nullable=False),
        sa.Column('total_return', sa.Numeric(12, 2), nullable=False),
        sa.Column('return_percentage', sa.Numeric(8, 4), nullable=False),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('winning_trades', sa.Integer(), nullable=True),
        sa.Column('losing_trades', sa.Integer(), nullable=True),
        sa.Column('win_rate', sa.Numeric(5, 2), nullable=True),
        sa.Column('max_drawdown', sa.Numeric(8, 4), nullable=True),
        sa.Column('min_capital', sa.Numeric(12, 2), nullable=True),
        sa.Column('sharpe_ratio', sa.Numeric(8, 4), nullable=True),
        sa.Column('profit_factor', sa.Numeric(8, 4), nullable=True),
        sa.Column('avg_trade_duration_minutes', sa.Integer(), nullable=True),
        sa.Column('best_trade_pnl', sa.Numeric(12, 2), nullable=True),
        sa.Column('worst_trade_pnl', sa.Numeric(12, 2), nullable=True),
        sa.Column('chart_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['job_id'], ['backtest_jobs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('job_id')
    )

    # Create trades table
    op.create_table(
        'trades',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('job_id', sa.String(36), nullable=False),
        sa.Column('trade_sequence', sa.Integer(), nullable=False),
        sa.Column('trade_type', sa.String(10), nullable=False),
        sa.Column('symbol', sa.String(20), nullable=False),
        sa.Column('trade_time', sa.DateTime(), nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('brokerage_fee', sa.Numeric(8, 2), nullable=True, server_default='0'),
        sa.Column('capital_after', sa.Numeric(12, 2), nullable=False),
        sa.Column('pnl', sa.Numeric(12, 2), nullable=True),
        sa.Column('pnl_percentage', sa.Numeric(8, 4), nullable=True),
        sa.Column('z_score', sa.Numeric(8, 4), nullable=True),
        sa.Column('sma', sa.Numeric(10, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['job_id'], ['backtest_jobs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better query performance
    op.create_index(op.f('ix_backtest_jobs_algorithm_id'), 'backtest_jobs', ['algorithm_id'], unique=False)
    op.create_index(op.f('ix_backtest_jobs_status'), 'backtest_jobs', ['status'], unique=False)
    op.create_index(op.f('ix_backtest_results_job_id'), 'backtest_results', ['job_id'], unique=False)
    op.create_index(op.f('ix_trades_job_id'), 'trades', ['job_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_trades_job_id'), table_name='trades')
    op.drop_index(op.f('ix_backtest_results_job_id'), table_name='backtest_results')
    op.drop_index(op.f('ix_backtest_jobs_status'), table_name='backtest_jobs')
    op.drop_index(op.f('ix_backtest_jobs_algorithm_id'), table_name='backtest_jobs')
    op.drop_table('trades')
    op.drop_table('backtest_results')
    op.drop_table('backtest_jobs')
    op.drop_table('algorithms')
