"""empty message

Revision ID: 8d47782a0098
Revises: f252d1ad8d23
Create Date: 2019-02-04 21:20:00.842394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d47782a0098'
down_revision = 'f252d1ad8d23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ElementAttributeTemplate', sa.Column('LookupId', sa.Integer(), nullable=True))
    op.add_column('ElementAttributeTemplate', sa.Column('UnitOfMeasurementId', sa.Integer(), nullable=True))
    op.create_foreign_key('FK__UnitOfMeasurement$CanBeUsedIn$ElementAttributeTemplate', 'ElementAttributeTemplate', 'UnitOfMeasurement', ['UnitOfMeasurementId'], ['UnitOfMeasurementId'])
    op.create_foreign_key('FK__Lookup$CanBeUsedIn$ElementAttributeTemplate', 'ElementAttributeTemplate', 'Lookup', ['LookupId'], ['LookupId'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('FK__Lookup$CanBeUsedIn$ElementAttributeTemplate', 'ElementAttributeTemplate', type_='foreignkey')
    op.drop_constraint('FK__UnitOfMeasurement$CanBeUsedIn$ElementAttributeTemplate', 'ElementAttributeTemplate', type_='foreignkey')
    op.drop_column('ElementAttributeTemplate', 'UnitOfMeasurementId')
    op.drop_column('ElementAttributeTemplate', 'LookupId')
    # ### end Alembic commands ###