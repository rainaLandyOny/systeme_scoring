"""create_training_data_table

Revision ID: b3f37cda6c32
Revises: 
Create Date: 2025-05-16 13:41:41.333230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3f37cda6c32'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'training_data',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('model_key', sa.String(50), nullable=False),
        sa.Column('features', sa.JSON(), nullable=False),
        sa.Column('true_score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('is_used', sa.Boolean(), server_default='false')
    )

def downgrade():
    op.drop_table('training_data')
