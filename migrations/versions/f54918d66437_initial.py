"""initial

Revision ID: f54918d66437
Revises: 
Create Date: 2022-04-29 23:32:50.244819

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from enum import Enum

# revision identifiers, used by Alembic.
revision = 'f54918d66437'
down_revision = None
branch_labels = None
depends_on = None


class OrderStatusEnum(Enum):
    INITIAL = "initial"
    PROCESSING = "processing"
    CANCELED = "canceled"
    DELIVERED = "delivered"


class ProductStatusEnum(Enum):
    NORMAL = "normal"
    ARCHIVED = "archived"


product_status_enum_vals = [val.name for val in ProductStatusEnum]
order_status_enum_vals = [val.name for val in OrderStatusEnum]


def upgrade():
    product_status_enum = postgresql.ENUM(*product_status_enum_vals, name='product_status_enum')
    product_status_enum.create(op.get_bind())
    order_status_enum = postgresql.ENUM(*order_status_enum_vals, name='order_status_enum')
    order_status_enum.create(op.get_bind())

    op.create_table(
        'orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', postgresql.ENUM(*order_status_enum_vals, name='order_status_enum',
                                            create_type=False), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'products',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('cost', sa.Integer(), server_default='0', nullable=False),
        sa.Column('price', sa.Integer(), server_default='0', nullable=False),
        sa.Column('stock', sa.Integer(), server_default='0', nullable=False),
        sa.Column('status', postgresql.ENUM(*product_status_enum_vals, name='product_status_enum',
                                            create_type=False), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'order_products',
        sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('cost', sa.Integer(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('count', sa.Integer(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('order_id', 'product_id')
    )


def downgrade():
    op.drop_table('order_products')
    op.drop_table('products')
    op.drop_table('orders')

    product_status_enum = postgresql.ENUM(*product_status_enum_vals, name='product_status_enum')
    product_status_enum.drop(op.get_bind())
    order_status_enum = postgresql.ENUM(*order_status_enum_vals, name='order_status_enum')
    order_status_enum.drop(op.get_bind())
