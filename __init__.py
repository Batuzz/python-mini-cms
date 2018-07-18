import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
"""
This web application is a small CMS. Main features are
    - dynamically working menu (with implemented possibility of creating submenus)
    - dynamic page content (one image and one piece of text per page / subpage)
    - gathering quiz/poll data (I mean: the answer that anonymous user chose in the form and confirm that choice)
    - ability of creating quizzes or polls and results of it presented in charts:
        + variable amount of quizzes/polls
        + variable amount of questions
        + variable amount of answer options
    - all the elements are easy to manage (add, edit, delete):
        - menu
        - submenus
        - pages
        - quizzes
        - quiz questions
        - quiz answer options
    - CMS' admin panel is accessible only after login via OPENID provider
    - dual language interface
    - ORM included
    - MVT architecture of application
"""
app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models

app.run()
