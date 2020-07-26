"""Initial migration.

Revision ID: b13236977763
Revises: 
Create Date: 2020-07-12 12:00:08.014674

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b13236977763'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Enterprise',
    sa.Column('EnterpriseId', sa.Integer(), nullable=False),
    sa.Column('Abbreviation', sa.String(length=10), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('EnterpriseId'),
    sa.UniqueConstraint('Abbreviation', name='AK__Abbreviation'),
    sa.UniqueConstraint('Name', name='AK__Name')
    )
    op.create_table('EventFrameGroup',
    sa.Column('EventFrameGroupId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('EventFrameGroupId'),
    sa.UniqueConstraint('Name', name='AK__Name')
    )
    op.create_index('IX__Name', 'EventFrameGroup', ['Name'], unique=False)
    op.create_table('Role',
    sa.Column('RoleId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('Permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('RoleId'),
    sa.UniqueConstraint('Name', name='AK__Name')
    )
    op.create_index('IX__Name', 'Role', ['Name'], unique=False)
    op.create_table('UnitOfMeasurement',
    sa.Column('UnitOfMeasurementId', sa.Integer(), nullable=False),
    sa.Column('Abbreviation', sa.String(length=15), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('UnitOfMeasurementId'),
    sa.UniqueConstraint('Abbreviation', 'Name', name='AK__Abbreviation__Name')
    )
    op.create_table('Lookup',
    sa.Column('LookupId', sa.Integer(), nullable=False),
    sa.Column('EnterpriseId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['EnterpriseId'], ['Enterprise.EnterpriseId'], name='FK__Enterprise$Have$Lookup'),
    sa.PrimaryKeyConstraint('LookupId'),
    sa.UniqueConstraint('EnterpriseId', 'Name', name='AK__EnterpriseId__Name')
    )
    op.create_table('Site',
    sa.Column('SiteId', sa.Integer(), nullable=False),
    sa.Column('Abbreviation', sa.String(length=10), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('EnterpriseId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['EnterpriseId'], ['Enterprise.EnterpriseId'], name='FK__Enterprise$Have$Site'),
    sa.PrimaryKeyConstraint('SiteId'),
    sa.UniqueConstraint('Abbreviation', 'EnterpriseId', name='AK__Abbreviation__EnterpriseId'),
    sa.UniqueConstraint('EnterpriseId', 'Name', name='AK__EnterpriseId__Name')
    )
    op.create_table('User',
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('Enabled', sa.Boolean(), nullable=False),
    sa.Column('LastMessageReadTimestamp', mysql.DATETIME(fsp=6), nullable=True),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('PasswordHash', sa.String(length=128), nullable=True),
    sa.Column('RoleId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['RoleId'], ['Role.RoleId'], name='FK__Role$Have$User'),
    sa.PrimaryKeyConstraint('UserId'),
    sa.UniqueConstraint('Name', name='AK__Name')
    )
    op.create_index('IX__Name', 'User', ['Name'], unique=False)
    op.create_table('Area',
    sa.Column('AreaId', sa.Integer(), nullable=False),
    sa.Column('Abbreviation', sa.String(length=10), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('SiteId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['SiteId'], ['Site.SiteId'], name='FK__Site$Have$Area'),
    sa.PrimaryKeyConstraint('AreaId'),
    sa.UniqueConstraint('Abbreviation', 'SiteId', name='AK__Abbreviation__SiteId'),
    sa.UniqueConstraint('Name', 'SiteId', name='AK__Name__SiteId')
    )
    op.create_table('ElementTemplate',
    sa.Column('ElementTemplateId', sa.Integer(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('SiteId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['SiteId'], ['Site.SiteId'], name='FK__Site$Have$ElementTemplate'),
    sa.PrimaryKeyConstraint('ElementTemplateId'),
    sa.UniqueConstraint('Name', 'SiteId', name='AK__Name__SiteId')
    )
    op.create_table('LookupValue',
    sa.Column('LookupValueId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('Selectable', sa.Boolean(), nullable=False),
    sa.Column('LookupId', sa.Integer(), nullable=False),
    sa.Column('Value', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['LookupId'], ['Lookup.LookupId'], name='FK__Lookup$Have$LookupValue'),
    sa.PrimaryKeyConstraint('LookupValueId'),
    sa.UniqueConstraint('LookupId', 'Name', name='AK__LookupId__Name'),
    sa.UniqueConstraint('LookupId', 'Value', name='AK__LookupId__Value')
    )
    op.create_table('Message',
    sa.Column('MessageId', sa.Integer(), nullable=False),
    sa.Column('Body', sa.Text(), nullable=False),
    sa.Column('RecipientId', sa.Integer(), nullable=False),
    sa.Column('SenderId', sa.Integer(), nullable=False),
    sa.Column('Timestamp', mysql.DATETIME(fsp=6), nullable=False),
    sa.ForeignKeyConstraint(['RecipientId'], ['User.UserId'], name='FK__User$Receive$Message'),
    sa.ForeignKeyConstraint(['SenderId'], ['User.UserId'], name='FK__User$Send$Message'),
    sa.PrimaryKeyConstraint('MessageId')
    )
    op.create_index('IX__RecipientId__Timestamp', 'Message', ['RecipientId', 'Timestamp'], unique=False)
    op.create_table('Note',
    sa.Column('NoteId', sa.Integer(), nullable=False),
    sa.Column('Note', sa.Text(), nullable=False),
    sa.Column('Timestamp', mysql.DATETIME(fsp=6), nullable=False),
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['UserId'], ['User.UserId'], name='FK__User$AddOrEdit$Note'),
    sa.PrimaryKeyConstraint('NoteId')
    )
    op.create_index('IX__Timestamp', 'Note', ['Timestamp'], unique=False)
    op.create_table('Notification',
    sa.Column('NotificationId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=128), nullable=False),
    sa.Column('Payload', sa.Text(), nullable=True),
    sa.Column('UnixTimestamp', mysql.DOUBLE(), nullable=False),
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['UserId'], ['User.UserId'], name='FK__User$Have$Notification'),
    sa.PrimaryKeyConstraint('NotificationId')
    )
    op.create_index('IX__UserId__Name__UnixTimestamp', 'Notification', ['UserId', 'Name', 'UnixTimestamp'], unique=False)
    op.create_table('Element',
    sa.Column('ElementId', sa.Integer(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('ElementTemplateId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('TagAreaId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ElementTemplateId'], ['ElementTemplate.ElementTemplateId'], name='FK__ElementTemplate$Have$Element'),
    sa.ForeignKeyConstraint(['TagAreaId'], ['Area.AreaId'], name='FK__Area$House$ManagedElementTag'),
    sa.PrimaryKeyConstraint('ElementId'),
    sa.UniqueConstraint('ElementTemplateId', 'Name', name='AK__ElementTemplateId__Name')
    )
    op.create_table('ElementAttributeTemplate',
    sa.Column('ElementAttributeTemplateId', sa.Integer(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('ElementTemplateId', sa.Integer(), nullable=False),
    sa.Column('LookupId', sa.Integer(), nullable=True),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('UnitOfMeasurementId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ElementTemplateId'], ['ElementTemplate.ElementTemplateId'], name='FK__ElementTemplate$Have$ElementAttributeTemplate'),
    sa.ForeignKeyConstraint(['LookupId'], ['Lookup.LookupId'], name='FK__Lookup$CanBeUsedIn$ElementAttributeTemplate'),
    sa.ForeignKeyConstraint(['UnitOfMeasurementId'], ['UnitOfMeasurement.UnitOfMeasurementId'], name='FK__UnitOfMeasurement$CanBeUsedIn$ElementAttributeTemplate'),
    sa.PrimaryKeyConstraint('ElementAttributeTemplateId'),
    sa.UniqueConstraint('ElementTemplateId', 'Name', name='AK__ElementTemplateId__Name')
    )
    op.create_table('EventFrameTemplate',
    sa.Column('EventFrameTemplateId', sa.Integer(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('ElementTemplateId', sa.Integer(), nullable=True),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('Order', sa.Integer(), nullable=False),
    sa.Column('ParentEventFrameTemplateId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ElementTemplateId'], ['ElementTemplate.ElementTemplateId'], name='FK__ElementTemplate$Have$EventFrameTemplate'),
    sa.ForeignKeyConstraint(['ParentEventFrameTemplateId'], ['EventFrameTemplate.EventFrameTemplateId'], name='FK__EventFrameTemplate$CanHave$EventFrameTemplate'),
    sa.PrimaryKeyConstraint('EventFrameTemplateId'),
    sa.UniqueConstraint('ElementTemplateId', 'Name', name='AK__ElementTemplateId_Name'),
    sa.UniqueConstraint('Name', 'ParentEventFrameTemplateId', name='AK__Name_ParentEventFrameTemplateId'),
    sa.UniqueConstraint('Order', 'ParentEventFrameTemplateId', name='AK__Order_ParentEventFrameTemplateId')
    )
    op.create_table('Tag',
    sa.Column('TagId', sa.Integer(), nullable=False),
    sa.Column('AreaId', sa.Integer(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('LookupId', sa.Integer(), nullable=True),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('UnitOfMeasurementId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['AreaId'], ['Area.AreaId'], name='FK__Area$Have$Tag'),
    sa.ForeignKeyConstraint(['LookupId'], ['Lookup.LookupId'], name='FK__Lookup$CanBeUsedIn$Tag'),
    sa.ForeignKeyConstraint(['UnitOfMeasurementId'], ['UnitOfMeasurement.UnitOfMeasurementId'], name='FK__UnitOfMeasurement$CanBeUsedIn$Tag'),
    sa.PrimaryKeyConstraint('TagId'),
    sa.UniqueConstraint('AreaId', 'Name', name='AK__AreaId__Name')
    )
    op.create_table('ElementAttribute',
    sa.Column('ElementAttributeId', sa.Integer(), nullable=False),
    sa.Column('ElementAttributeTemplateId', sa.Integer(), nullable=False),
    sa.Column('ElementId', sa.Integer(), nullable=False),
    sa.Column('TagId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ElementAttributeTemplateId'], ['ElementAttributeTemplate.ElementAttributeTemplateId'], name='FK__ElementAttributeTemplate$Have$ElementAttribute'),
    sa.ForeignKeyConstraint(['ElementId'], ['Element.ElementId'], name='FK__Element$Have$ElementAttribute'),
    sa.ForeignKeyConstraint(['TagId'], ['Tag.TagId'], name='FK__Tag$Have$ElementAttribute'),
    sa.PrimaryKeyConstraint('ElementAttributeId'),
    sa.UniqueConstraint('ElementAttributeTemplateId', 'ElementId', name='AK__ElementAttributeTemplateId__ElementId')
    )
    op.create_table('EventFrame',
    sa.Column('EventFrameId', sa.Integer(), nullable=False),
    sa.Column('ElementId', sa.Integer(), nullable=True),
    sa.Column('EndTimestamp', mysql.DATETIME(fsp=6), nullable=True),
    sa.Column('EventFrameTemplateId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('ParentEventFrameId', sa.Integer(), nullable=True),
    sa.Column('StartTimestamp', mysql.DATETIME(fsp=6), nullable=False),
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ElementId'], ['Element.ElementId'], name='FK__Element$Have$EventFrame'),
    sa.ForeignKeyConstraint(['EventFrameTemplateId'], ['EventFrameTemplate.EventFrameTemplateId'], name='FK__EventFrameTemplate$Have$EventFrame'),
    sa.ForeignKeyConstraint(['ParentEventFrameId'], ['EventFrame.EventFrameId'], name='FK__EventFrame$CanHave$EventFrame'),
    sa.ForeignKeyConstraint(['UserId'], ['User.UserId'], name='FK__User$AddOrEdit$EventFrame'),
    sa.PrimaryKeyConstraint('EventFrameId'),
    sa.UniqueConstraint('ElementId', 'EventFrameTemplateId', 'StartTimestamp', name='AK__ElementId_EventFrameTemplateId_StartTimestamp')
    )
    op.create_index('IX__StartTimestamp__EndTimestamp', 'EventFrame', ['StartTimestamp', 'EndTimestamp'], unique=False)
    op.create_table('EventFrameAttributeTemplate',
    sa.Column('EventFrameAttributeTemplateId', sa.Integer(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('DefaultEndValue', sa.Float(), nullable=True),
    sa.Column('DefaultStartValue', sa.Float(), nullable=True),
    sa.Column('EventFrameTemplateId', sa.Integer(), nullable=False),
    sa.Column('LookupId', sa.Integer(), nullable=True),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('UnitOfMeasurementId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['EventFrameTemplateId'], ['EventFrameTemplate.EventFrameTemplateId'], name='FK__EventFrameTemplate$Have$EventFrameAttributeTemplate'),
    sa.ForeignKeyConstraint(['LookupId'], ['Lookup.LookupId'], name='FK__Lookup$CanBeUsedIn$EventFrameAttributeTemplate'),
    sa.ForeignKeyConstraint(['UnitOfMeasurementId'], ['UnitOfMeasurement.UnitOfMeasurementId'], name='FK__UnitOfMeasurement$CanBeUsedIn$EventFrameAttributeTemplate'),
    sa.PrimaryKeyConstraint('EventFrameAttributeTemplateId'),
    sa.UniqueConstraint('EventFrameTemplateId', 'Name', name='AK__EventFrameTemplateId__Name')
    )
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
    op.create_table('TagValue',
    sa.Column('TagValueId', sa.Integer(), nullable=False),
    sa.Column('TagId', sa.Integer(), nullable=False),
    sa.Column('Timestamp', mysql.DATETIME(fsp=6), nullable=False),
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('Value', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['TagId'], ['Tag.TagId'], name='FK__Tag$Have$TagValue'),
    sa.ForeignKeyConstraint(['UserId'], ['User.UserId'], name='FK__User$AddOrEdit$TagValue'),
    sa.PrimaryKeyConstraint('TagValueId'),
    sa.UniqueConstraint('TagId', 'Timestamp', name='AK__TagId__Timestamp')
    )
    op.create_index('IX__Timestamp', 'TagValue', ['Timestamp'], unique=False)
    op.create_table('EventFrameAttribute',
    sa.Column('EventFrameAttributeId', sa.Integer(), nullable=False),
    sa.Column('ElementId', sa.Integer(), nullable=False),
    sa.Column('EventFrameAttributeTemplateId', sa.Integer(), nullable=False),
    sa.Column('TagId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ElementId'], ['Element.ElementId'], name='FK__Element$Have$EventFrameAttribute'),
    sa.ForeignKeyConstraint(['EventFrameAttributeTemplateId'], ['EventFrameAttributeTemplate.EventFrameAttributeTemplateId'], name='FK__EventFrameAttributeTemplate$Have$EventFrameAttribute'),
    sa.ForeignKeyConstraint(['TagId'], ['Tag.TagId'], name='FK__Tag$Have$EventFrameAttribute'),
    sa.PrimaryKeyConstraint('EventFrameAttributeId'),
    sa.UniqueConstraint('EventFrameAttributeTemplateId', 'ElementId', name='AK__EventFrameAttributeTemplateId__ElementId')
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
    op.create_table('EventFrameEventFrameGroup',
    sa.Column('EventFrameEventFrameGroupId', sa.Integer(), nullable=False),
    sa.Column('EventFrameGroupId', sa.Integer(), nullable=False),
    sa.Column('EventFrameId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['EventFrameGroupId'], ['EventFrameGroup.EventFrameGroupId'], name='FK__EventFrameGroup$Have$EventFrameEventFrameGroup'),
    sa.ForeignKeyConstraint(['EventFrameId'], ['EventFrame.EventFrameId'], name='FK__EventFrame$Have$EventFrameEventFrameGroup'),
    sa.PrimaryKeyConstraint('EventFrameEventFrameGroupId'),
    sa.UniqueConstraint('EventFrameGroupId', 'EventFrameId', name='AK__EventFrameGroupId__EventFrameId')
    )
    op.create_table('EventFrameNote',
    sa.Column('EventFrameId', sa.Integer(), nullable=False),
    sa.Column('NoteId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['EventFrameId'], ['EventFrame.EventFrameId'], name='FK__EventFrame$CanHave$EventFrameNote'),
    sa.ForeignKeyConstraint(['NoteId'], ['Note.NoteId'], name='FK__Note$CanBe$EventFrameNote'),
    sa.PrimaryKeyConstraint('NoteId', 'EventFrameId')
    )
    op.create_table('TagValueNote',
    sa.Column('NoteId', sa.Integer(), nullable=False),
    sa.Column('TagValueId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['NoteId'], ['Note.NoteId'], name='FK__Note$CanBe$TagValueNote'),
    sa.ForeignKeyConstraint(['TagValueId'], ['TagValue.TagValueId'], name='FK__TagValue$CanHave$TagValueNote'),
    sa.PrimaryKeyConstraint('NoteId', 'TagValueId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TagValueNote')
    op.drop_table('EventFrameNote')
    op.drop_table('EventFrameEventFrameGroup')
    op.drop_table('EventFrameAttributeTemplateEventFrameTemplateView')
    op.drop_table('EventFrameAttribute')
    op.drop_index('IX__Timestamp', table_name='TagValue')
    op.drop_table('TagValue')
    op.drop_table('EventFrameTemplateView')
    op.drop_table('EventFrameAttributeTemplate')
    op.drop_index('IX__StartTimestamp__EndTimestamp', table_name='EventFrame')
    op.drop_table('EventFrame')
    op.drop_table('ElementAttribute')
    op.drop_table('Tag')
    op.drop_table('EventFrameTemplate')
    op.drop_table('ElementAttributeTemplate')
    op.drop_table('Element')
    op.drop_index('IX__UserId__Name__UnixTimestamp', table_name='Notification')
    op.drop_table('Notification')
    op.drop_index('IX__Timestamp', table_name='Note')
    op.drop_table('Note')
    op.drop_index('IX__RecipientId__Timestamp', table_name='Message')
    op.drop_table('Message')
    op.drop_table('LookupValue')
    op.drop_table('ElementTemplate')
    op.drop_table('Area')
    op.drop_index('IX__Name', table_name='User')
    op.drop_table('User')
    op.drop_table('Site')
    op.drop_table('Lookup')
    op.drop_table('UnitOfMeasurement')
    op.drop_index('IX__Name', table_name='Role')
    op.drop_table('Role')
    op.drop_index('IX__Name', table_name='EventFrameGroup')
    op.drop_table('EventFrameGroup')
    op.drop_table('Enterprise')
    # ### end Alembic commands ###