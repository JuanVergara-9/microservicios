"""create inventario table

Revision ID: 50feea5f023e
Revises: 
Create Date: 2024-12-04 10:21:13.571301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50feea5f023e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('descripcion', sa.String(length=200), nullable=True),
    sa.Column('precio', sa.Float(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventario')
    # ### end Alembic commands ###