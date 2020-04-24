"""item count table

Revision ID: e45697e36ad6
Revises: faf1efa15bfa
Create Date: 2020-03-16 18:54:04.598634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e45697e36ad6'
down_revision = 'faf1efa15bfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('order_item_count', sa.Integer(), nullable=True))
    op.add_column('order', sa.Column('order_prod_id', sa.Integer(), nullable=True))
    op.drop_column('order', 'order_item_detail')
    op.drop_column('order', 'order_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('order_number', sa.INTEGER(), nullable=True))
    op.add_column('order', sa.Column('order_item_detail', sa.VARCHAR(), nullable=True))
    op.drop_column('order', 'order_prod_id')
    op.drop_column('order', 'order_item_count')
    # ### end Alembic commands ###
