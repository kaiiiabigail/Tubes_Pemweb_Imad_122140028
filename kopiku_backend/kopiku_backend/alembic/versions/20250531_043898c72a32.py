"""add_other_tables

Revision ID: 043898c72a32
Revises: initial_migration
Create Date: 2025-05-31 01:01:02.297000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '043898c72a32'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Buat tipe enum userrole terlebih dahulu
    userrole = postgresql.ENUM('ADMIN', 'USER', name='userrole', create_type=False)
    userrole.create(op.get_bind(), checkfirst=True)
    
    # Tambahkan kolom role dengan tipe userrole
    op.add_column('users', sa.Column('role', sa.Enum('ADMIN', 'USER', name='userrole'), nullable=False, server_default='USER'))
    
    # Buat tabel categories
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Buat tabel menu_items
    op.create_table('menu_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(length=200), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=False, server_default='true'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Buat tabel orders
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='PENDING'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Buat tabel order_items
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('menu_item_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['menu_item_id'], ['menu_items.id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('menu_items')
    op.drop_table('categories')
    op.drop_column('users', 'role')
    # Hapus tipe enum userrole
    userrole = postgresql.ENUM(name='userrole')
    userrole.drop(op.get_bind())
    # ### end Alembic commands ###
