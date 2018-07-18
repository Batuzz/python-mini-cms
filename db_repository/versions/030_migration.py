from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
quiz_answer = Table('quiz_answer', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('answer', VARCHAR),
    Column('answer_en', VARCHAR),
    Column('quiz_question_id', INTEGER),
)

quiz_answer_option = Table('quiz_answer_option', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('answer', String),
    Column('answer_en', String),
    Column('quiz_question_id', Integer),
)

quiz_user_answer = Table('quiz_user_answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('quiz_question_id', Integer),
    Column('quiz_answer_option_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['quiz_answer'].drop()
    post_meta.tables['quiz_answer_option'].create()
    post_meta.tables['quiz_user_answer'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['quiz_answer'].create()
    post_meta.tables['quiz_answer_option'].drop()
    post_meta.tables['quiz_user_answer'].drop()
