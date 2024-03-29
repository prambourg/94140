"""initial migration

Revision ID: ce8ef5c4a345
Revises: 
Create Date: 2023-09-29 21:55:34.292597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce8ef5c4a345'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('measurement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('humidity', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hello_asso_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('campagne', sa.String(length=100), nullable=True),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('email', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.Column('facebook', sa.String(length=100), nullable=True),
    sa.Column('instagram', sa.String(length=100), nullable=True),
    sa.Column('twitter', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('glucide', sa.Integer(), nullable=True),
    sa.Column('protide', sa.Integer(), nullable=True),
    sa.Column('lipide', sa.Integer(), nullable=True),
    sa.Column('sel', sa.Integer(), nullable=True),
    sa.Column('fiber', sa.Integer(), nullable=True),
    sa.Column('barcode', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('basket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('unit', sa.Integer(), nullable=True),
    sa.Column('basket_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['basket_id'], ['basket.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchase')
    op.drop_table('basket')
    op.drop_table('shop')
    op.drop_table('product')
    op.drop_table('order')
    op.drop_table('measurement')
    # ### end Alembic commands ###
