"""empty message

Revision ID: 4b3b407fa67d
Revises: 7e411683509e
Create Date: 2018-03-11 11:09:14.858797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b3b407fa67d'
down_revision = '7e411683509e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Role',
    sa.Column('RoleId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('Permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('RoleId'),
    sa.UniqueConstraint('Name', name='AK__Name')
    )
    op.create_index('IX_Name', 'Role', ['Name'], unique=False)
    op.create_table('User',
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('PasswordHash', sa.String(length=128), nullable=True),
    sa.Column('RoleId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['RoleId'], ['Role.RoleId'], name='FK__Role$Have$User'),
    sa.PrimaryKeyConstraint('UserId'),
    sa.UniqueConstraint('Name', name='AK__Name')
    )
    op.create_index('IX_Name', 'User', ['Name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('IX_Name', table_name='User')
    op.drop_table('User')
    op.drop_index('IX_Name', table_name='Role')
    op.drop_table('Role')
    # ### end Alembic commands ###