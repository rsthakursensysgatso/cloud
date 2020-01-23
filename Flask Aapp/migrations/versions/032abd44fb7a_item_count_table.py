"""item count table

Revision ID: 032abd44fb7a
Revises: bfe3a45b545a
Create Date: 2020-01-12 13:40:14.002784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '032abd44fb7a'
down_revision = 'bfe3a45b545a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subs', sa.Column('subs_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subs', 'subs_id')
    # ### end Alembic commands ###
