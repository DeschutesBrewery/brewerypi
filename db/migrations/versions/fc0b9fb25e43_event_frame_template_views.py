"""Event Frame Template Views.

Revision ID: fc0b9fb25e43
Revises: 9b71da09fc0b
Create Date: 2020-02-29 10:16:56.278715

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fc0b9fb25e43'
down_revision = '9b71da09fc0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('EventFrameTemplateView',
    sa.Column('EventFrameTemplateViewId', sa.Integer(), nullable=False),
    sa.Column('Dictionary', mysql.LONGTEXT(), nullable=True),
    sa.Column('Default', sa.Boolean(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('EventFrameTemplateId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['EventFrameTemplateId'], ['EventFrameTemplate.EventFrameTemplateId'], name='FK__EventFrameTemplate$Have$EventFrameTemplateView'),
    sa.PrimaryKeyConstraint('EventFrameTemplateViewId'),
    sa.UniqueConstraint('EventFrameTemplateId', 'Name', name='AK__EventFrameTemplateId_Name')
    )
    op.create_table('EventFrameAttributeTemplateEventFrameTemplateView',
    sa.Column('EventFrameAttributeTemplateEventFrameTemplateViewId', sa.Integer(), nullable=False),
    sa.Column('EventFrameAttributeTemplateId', sa.Integer(), nullable=False),
    sa.Column('EventFrameTemplateViewId', sa.Integer(), nullable=False),
    sa.Column('Order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['EventFrameAttributeTemplateId'], ['EventFrameAttributeTemplate.EventFrameAttributeTemplateId'], name='FK__EFAT$Have$EventFrameAttributeTemplateEventFrameTemplateView'),
    sa.ForeignKeyConstraint(['EventFrameTemplateViewId'], ['EventFrameTemplateView.EventFrameTemplateViewId'], name='FK__EFTV$Have$EventFrameAttributeTemplateEventFrameTemplateView'),
    sa.PrimaryKeyConstraint('EventFrameAttributeTemplateEventFrameTemplateViewId'),
    sa.UniqueConstraint('EventFrameAttributeTemplateId', 'EventFrameTemplateViewId', name='AK__EventFrameAttributeTemplateId__EventFrameTemplateViewId'),
    sa.UniqueConstraint('EventFrameTemplateViewId', 'Order', name='AK__EventFrameTemplateViewId__Order')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('EventFrameAttributeTemplateEventFrameTemplateView')
    op.drop_table('EventFrameTemplateView')
    # ### end Alembic commands ###
