from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from app.models import User, Menu, Quiz, QuizQuestion

"""
Contains all forms of an application.
Forms are used in templating.
"""


class LoginForm(Form):
    """
    Class representing Login Form.
    Contains fields:
        - OpenID provider (text field)
        - remember me (checkbox)
    """
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class MenuForm(Form):
    """
    Class representing Menu Form.
    Contains fields:
        - sequence (text field)
        - link (text field)
        - type (select box)
        - caption (text field)
        - caption_en (text field)
    """
    sequence = StringField('sequence')
    link = StringField('link', validators=[DataRequired()])
    choices = [("0", "Menu item"),
               ("1", "Submenu base")]
    type = SelectField('type', choices=choices, validators=[DataRequired()])
    caption = StringField('caption', validators=[DataRequired()])
    caption_en = StringField('caption_en', validators=[DataRequired()])


def menu_query():
    """
    Function gets all menus of type 1 (submenu bases) to prepare QuerySelectField in SubmenuForm
    :return: list
    """
    return Menu.query.filter_by(type=1).all()


class SubmenuForm(Form):
    """
    Class representing Submenu Form.
    Contains fields:
        - sequence (text field)
        - link (text field)
        - caption (text field)
        - caption_en (text field)
        - menu (select field)
    """
    sequence = StringField('sequence')
    link = StringField('link', validators=[DataRequired()])
    caption = StringField('caption', validators=[DataRequired()])
    caption_en = StringField('caption_en', validators=[DataRequired()])
    menu = QuerySelectField(query_factory=menu_query)


class PageForm(Form):
    """
    Class representing Page Form.
    Contains fields:
        - title (text field)
        - title_en (text field)
        - content (text area)
        - content_en (text area)
        - img_name (text field)
    """
    link = StringField('link', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    title_en = StringField('title_en', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    content_en = TextAreaField('content_en', validators=[DataRequired()])
    img_name = StringField('img_name', validators=[DataRequired()])


class QuizForm(Form):
    """
    Class representing Quiz Form.
    Contains field:
        - name (text field)
        - name_en (text field)
    """
    name = StringField('name', validators=[DataRequired()])
    name_en = StringField('name_en', validators=[DataRequired()])


def quiz_query():
    """
    Function gets all quizzes to prepare QuerySelectField in QuizQuestionForm.
    :return: list
    """
    return Quiz.query.all()


class QuizQuestionForm(Form):
    """
    Class representing Quiz Question Form.
    Contains fields:
        - question (text area)
        - question_en (text area)
        - quiz (select field)
    """
    question = TextAreaField('question', validators=[DataRequired()])
    question_en = TextAreaField('question_en', validators=[DataRequired()])
    quiz = QuerySelectField(query_factory=quiz_query)


def quiz_question_query():
    """
    Function gets all quiz questions to prepare QuerySelectField in QuizAnswerForm.
    :return: list
    """
    return QuizQuestion.query.all()


class QuizAnswerOptionForm(Form):
    """
    Class representing Quiz Answer Option Form.
    Contains fields:
        - answer (text area)
        - answer_en (text area)
        - quiz_question (select field)
    """
    answer = TextAreaField('answer', validators=[DataRequired()])
    answer_en = TextAreaField('answer_en', validators=[DataRequired()])
    quiz_question = QuerySelectField(query_factory=quiz_question_query)


class UserForm(Form):
    """
    Class representing User Form.
    Contains field:
        - nickname (text field)
    """
    nickname = StringField('nickname', validators=[DataRequired()])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        """
        Method checks if form fields are valid.
        :return: boolean
        """
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('This nickname is already in use. '
                                        'Please choose another one.')
            return False
        return True
