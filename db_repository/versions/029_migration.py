from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
quiz = Table('quiz', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
)

quiz_answer = Table('quiz_answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('answer', String),
    Column('answer_en', String),
    Column('quiz_question_id', Integer),
)

quiz_question = Table('quiz_question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('question', String(length=255)),
    Column('question_en', String(length=255)),
    Column('quiz_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['quiz'].create()
    post_meta.tables['quiz_answer'].create()
    post_meta.tables['quiz_question'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['quiz'].drop()
    post_meta.tables['quiz_answer'].drop()
    post_meta.tables['quiz_question'].drop()
