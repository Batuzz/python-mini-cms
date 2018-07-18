from app import db
from hashlib import md5

"""
Contains all models of an application.
It's a basis for creating database (ORM).
If you make any modifications over here, keep in mind that you have to use database_migrate script.
"""


class Page(db.Model):
    """
    Class representing Page model.
    Contains fields:
        - title - contains title of the Page
            e.g. title = "First page"
                 in view: <h1> {{ page.caption }} </h1>
        - title_en - contains title of the Page in english
            e.g. - see how to use title field
        - content - contains content of the Page
            e.g. content = "Lorem ipsum......."
                 in view: <div id="content"> {{ page.content }} </div>
        - content_en - contains content of the Page in english
            e.g. - see how to use content field
        - img_name - contains filename of an image
            e.g. in view: <img src="{{ page.content }}" />
    """
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(50))
    title = db.Column(db.String(50))
    title_en = db.Column(db.String(50))
    content = db.Column(db.Text)
    content_en = db.Column(db.Text)
    img_name = db.Column(db.String(50))

    def __repr__(self):
        """
        Method returns string representation of class, used for debugging and also useful in forms to display question
        element.
        :return: string
        """
        return self.title


class User(db.Model):
    """
    Class representing User model.
    Contains fields:
        - nickname - user's nickname
        - email - user's email address
        - permission - level of permission user has, the values depends on your choice.
            e.g. permission = 0 --> user has 0-level permission
                 permission = 100 --> user has highest-lever permission
        - register_date - the date when user was registered
    """
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    permission = db.Column(db.Integer)
    register_date = db.Column(db.DateTime)

    def avatar(self, size):
        """
        Method returns source of user's avatar stored in Gravatar.
        :return: string
        """
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(),
                                                                size)

    @staticmethod
    def make_unique_nickname(nickname):
        """
        Method returns unique nickname of new user.
        This process is crucial to avoid database errors.
        Loop adds a number after an original nickname and checks if it exists in database.
        If not - it returns new nickname.
        :param nickname: string
        :return: string
        """
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        """
        Method returns string representation of class, used for debugging.
        :return: string
        """
        return '<User %r, permission: %r>' % (self.nickname, self.permission)


class Menu(db.Model):
    """
    Class representing Menu model.
    Contains fields:
        - sequence - it decides about the order of menus
            e.g. Menu.query.order_by(Menu.sequence).all()
                will return menus in order we want them to be on the website.
        - link - the place we'll be redirected after clicking on menu's name in view
            e.g. link = "test_page"
                 in view: href="/page/{{ menu.link }}"
        - type - specifies if the menu contains submenus or it doesn't
            e.g. type = 0 - means it doesn't contain submenu
                 type = 1 - means it contains submenus
            It's useful when you're rendering navigation (the menu) dynamically in e.g. template.
        - caption - contains caption of the Menu
            e.g. caption = "Menu1"
                 in view: <li> {{ submenu.caption }} </li>
        - caption_en - contains caption of the Submenu in english
            e.g. - see how to use caption field
            
    It's related to Submenu model. (one-to-many relation)
    One Menu can have (0 to n) Submenus,
    but one Submenu can be matched with only one menu.
    """
    id = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(db.Integer, index=True, unique=True)
    link = db.Column(db.String(50))
    type = db.Column(db.Integer)
    caption = db.Column(db.String(50), index=True, unique=True)
    caption_en = db.Column(db.String(50), index=True, unique=True)

    def __repr__(self):
        """
        Method returns string representation of class, used for debugging and also useful in forms to display menu
        element.
        :return: string
        """
        return self.caption


class Submenu(db.Model):
    """
    Class representing Submenu model.
    Contains fields:
        - sequence - it decides about the order of submenus
            e.g. Submenu.query.order_by(Submenu.sequence).all()
                will return submenus in order we want them to be on the website.
        - link - the place we'll be redirected after clicking on submenu's name in view
            e.g. link = "test_page"
                 in view: href="/page/{{ submenu.link }}"
        - caption - contains caption of the Submenu
            e.g. caption = "Submenu1"
                 in view: <li> {{ submenu.caption }} </li>
        - caption_en - contains caption of the Submenu in english
            e.g. - see how to use caption field
            
    It's related to Menu model. (one-to-many relation)
    One Menu can have (0 to n) Submenus,
    but one Submenu can be matched with only one menu.
    """
    id = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(db.Integer, index=True)
    link = db.Column(db.String(50))
    caption = db.Column(db.String(50), index=True, unique=True)
    caption_en = db.Column(db.String(50), index=True, unique=True)
    section_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menu = db.relationship('Menu',
                           backref=db.backref('submenus', lazy='dynamic'))

    def __init__(self, sequence, link, caption, caption_en, menu):
        self.sequence = sequence
        self.link = link
        self.caption = caption
        self.caption_en = caption_en
        self.menu = menu


class Quiz(db.Model):
    """
    Class representing Quiz model.
    
    Contains:
        - name of a Quiz
        - name of a Quiz in english
 
    It's matched with QuizQuestion - one Quiz can have (0 to n) questions,
    but one question can be matched only with one Quiz. (one-to-many relation)
    """
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    name_en = db.Column(db.String(100))

    def __repr__(self):
        """
        Method returns string representation of class, used for debugging and also useful in forms to display quiz
        element.
        :return: string
        """
        return self.name


class QuizQuestion(db.Model):
    """
    Class representing QuizQuestion model.
    It's a single question of a quiz - simply added question's content and english content.
    
    Contains the question content in two languages (I also mean: in 2 fields - question & question_en).
    It's matched with:
        - Quiz - one Quiz can have (0 to n) questions,
                but one question can be matched only with one Quiz.
                (one-to-many relation)
        - QuizAnswerOption - one QuizQuestion can have (0 to n) answers,
                but one QuizAnswer can be matched only with one QuizQuestion.
                (one-to-many relation)
    Other tables (models) matched with QuizQuestion:
        - QuizUserAnswer - check QuizUserAnswer docs.
    """
    __tablename__ = 'quiz_question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255))
    question_en = db.Column(db.String(255))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    quiz = db.relationship('Quiz',
                           backref=db.backref('questions', lazy='dynamic'))

    def __init__(self, question, question_en, quiz):
        self.question = question
        self.question_en = question_en
        self.quiz = quiz

    def __repr__(self):
        """
        Method returns string representation of class, used for debugging and also useful in forms to display question
        element.
        :return: string
        """
        return self.question


class QuizAnswerOption(db.Model):
    """
    Class representing QuizAnswerOption model.
    It's a single answer option of a quiz - simply added answer's content (answer) and english content (answer_en).
    Contains the answer content in two languages (I also mean - in 2 fields: answer & answer_en).
    It's matched with:
        - QuizQuestion - one QuizQuestion can have (0 to n) answers,
                but one answer can be matched only with one QuizQuestion.
                (one-to-many relation)
    Other tables (models) matched with QuizQuestion:
        - QuizUserAnswer - check QuizUserAnswer docs.
    """
    __tablename__ = 'quiz_answer_option'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    answer_en = db.Column(db.String)
    quiz_question_id = db.Column(db.Integer, db.ForeignKey('quiz_question.id'))
    quiz_question = db.relationship('QuizQuestion',
                                    backref=db.backref('answers', lazy='dynamic'))

    def __init__(self, answer, answer_en, quiz_question):
        self.answer = answer
        self.answer_en = answer_en
        self.quiz_question = quiz_question


class QuizUserAnswer(db.Model):
    """
    Class representing QuizUserAnswer model.
    It's a single choice of a person that fills the quiz.
    Contains QuizQuestion and QuizAnswerOption.
    It's matching one QuizQuestion with one QuizAnswerOption. (many-to-many relation)
    The quiz is anonymous so it don't need any user matched with this.
    """
    id = db.Column(db.Integer, primary_key=True)
    quiz_question_id = db.Column(db.Integer, db.ForeignKey('quiz_question.id'))
    quiz_question = db.relationship('QuizQuestion',
                                    backref=db.backref('user_question', lazy='dynamic'))
    quiz_answer_option_id = db.Column(db.Integer, db.ForeignKey('quiz_answer_option.id'))
    quiz_answer_option = db.relationship('QuizAnswerOption',
                                         backref=db.backref('user_answer', lazy='dynamic'))

    def __repr__(self):
        return 'Question: %s \nAnswer: %s' % (self.quiz_question.question, self.quiz_answer_option.answer)
