from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu = Table('menu', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('index', INTEGER),
    Column('link', VARCHAR(length=50)),
    Column('type', INTEGER),
    Column('caption', VARCHAR(length=50)),
    Column('caption_en', VARCHAR(length=50)),
)

menu = Table('menu', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('sequence', Integer),
    Column('link', String(length=50)),
    Column('type', Integer),
    Column('caption', String(length=50)),
    Column('caption_en', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['menu'].columns['index'].drop()
    post_meta.tables['menu'].columns['sequence'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['menu'].columns['index'].create()
    post_meta.tables['menu'].columns['sequence'].drop()
