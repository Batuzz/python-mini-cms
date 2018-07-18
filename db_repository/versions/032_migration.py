from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
page = Table('page', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('link', String(length=50)),
    Column('title', String(length=50)),
    Column('title_en', String(length=50)),
    Column('content', Text),
    Column('content_en', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['page'].columns['link'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['page'].columns['link'].drop()
