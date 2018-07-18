from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
submenu = Table('submenu', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('sequence', INTEGER),
    Column('link', VARCHAR(length=50)),
    Column('caption', VARCHAR(length=50)),
    Column('caption_en', VARCHAR(length=50)),
    Column('section', INTEGER),
)

submenu = Table('submenu', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('sequence', Integer),
    Column('link', String(length=50)),
    Column('caption', String(length=50)),
    Column('caption_en', String(length=50)),
    Column('section_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['submenu'].columns['section'].drop()
    post_meta.tables['submenu'].columns['section_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['submenu'].columns['section'].create()
    post_meta.tables['submenu'].columns['section_id'].drop()
