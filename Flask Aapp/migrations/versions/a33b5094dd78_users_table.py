"""users table

Revision ID: a33b5094dd78
Revises: 2718d2160a48
Create Date: 2019-12-01 19:35:05.643888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a33b5094dd78'
down_revision = '2718d2160a48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('prod_id', sa.Integer(), nullable=False),
    sa.Column('prod_name', sa.String(length=64), nullable=True),
    sa.Column('prod_cost', sa.Integer(), nullable=True),
    sa.Column('prod_desc', sa.String(length=140), nullable=True),
    sa.Column('image_filename', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('prod_id')
    )
    op.create_index(op.f('ix_cart_prod_name'), 'cart', ['prod_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cart_prod_name'), table_name='cart')
    op.drop_table('cart')
    # ### end Alembic commands ###
