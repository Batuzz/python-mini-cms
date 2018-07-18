# coding=utf-8
import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, UserForm, MenuForm, PageForm, SubmenuForm, QuizForm, QuizQuestionForm, \
    QuizAnswerOptionForm
from .models import User, Menu, Page, Submenu, Quiz, QuizQuestion, QuizAnswerOption, QuizUserAnswer

"""
This is main application controller.
It connects Models with Templates (MVT architecture of application).
"""


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    """
    Function checks if language is in session.
    If so - prepares main page.
    If not - prepares language choice page.
    :return: HTML page
    """
    if 'lang' not in session:
        return render_template('lang.html')
    page = Page.query.filter_by(link="index").first()
    user = g.user
    menu = Menu.query.order_by(Menu.sequence).all()
    return render_template('index.html',
                           user=user,
                           menu=menu,
                           const=app.config['LANG_CONSTS'],
                           page=page)


@app.route('/index/<language>')
def lang(language):
    """
    Function saves language in session.
    :param language: string
    :return: HTML page
    """
    session['lang'] = language
    return redirect(url_for('index'))


@app.route('/login', Functions=['GET', 'POST'])
@oid.loginhandler
def login():
    """
    Function checks if user is logged in and authenticated.
    If so redirects him to index (main) page.
    If not - checks if the login form is valid
        If so - tries to login via OpenID system.
        If not - returns login page.
    :return: HTML page
    """
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'],
                           const=app.config['LANG_CONSTS'])


@oid.after_login
def after_login(resp):
    """
    Function checks if login went right.
    If so - passes user through. If 'remember_me' option was checked, saves login data in browser.
    Redirects to index.html page.
    If not - flashes a message about wrong login data and redirects to login page.
    
    :param resp: response
    :return: HTML page
    """
    user = User.query.filter_by(email=resp.email).first()
    if resp.email is None or resp.email == "" or user is None:
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or render_template('adminpanel_loading.html'))


@app.route('/logout')
def logout():
    """
    This Function logs user out.
    :return: HTML page
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/page/<index>')
def show_page(index):
    """
    Function prepares HTML content of single page.
    Index specifies a link of page (or an ID if link is not found).
    Gets necessary variables and send it as parameter to function render_template().
    
    If getting a page fails, returns page 404. 
    :param index: link or ID of page
    :return: HTML page
    """
    menu = Menu.query.order_by(Menu.sequence).all()
    page = Page.query.filter_by(link=index).first()

    if page is None:
        page = Page.query.filter_by(id=index).first()
        if page is None:
            return render_template('404.html',
                                   const=app.config['LANG_CONSTS']), 404

    return render_template('page.html',
                           menu=menu,
                           page=page,
                           const=app.config['LANG_CONSTS'])


@app.route('/user/<nickname>')
def user(nickname):
    """
    Function checks if user with nickname specified in parameter exists in database.
    If so - prepares page that contains his info.
    If not - prints that user with such nickname doesn't exist.
    :param nickname: user's nickname 
    :return: HTML page
    """
    user_ = User.query.filter_by(nickname=nickname).first()
    menu = Menu.query.order_by(Menu.sequence).all()
    if user_ is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    return render_template('user.html',
                           user=user_,
                           const=app.config['LANG_CONSTS'],
                           menu=menu)


@app.route('/user/edit', Functions=['GET', 'POST'])
@login_required
def user_edit():
    """
    Function checks if user's form (forms.UserForm) is valid.
    If so edits the data specified in form of currently logged in user.
    If not - prepares page that contains filled UserForm with current data.
    :return: HTML page
    """
    menu = Menu.query.order_by(Menu.sequence).all()
    form = UserForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user_edit'))
    else:
        form.nickname.data = g.user.nickname
    return render_template('user_edit.html',
                           form=form,
                           menu=menu,
                           const=app.config['LANG_CONSTS'])


@app.route('/admin/menu', Functions=['GET', 'POST'])
@login_required
def add_menu():
    """
    Function prepares page with empty MenuForm and table of Menus that already exist in database. If validation 
    passes well - new Menu with data specified in form is added to database. 
    If not - page is prepared again, with pre-filled form and errors due to which validation didn't pass through.
    :return: HTML page 
    """
    form = MenuForm()
    menu = Menu.query.order_by(Menu.sequence).all()
    if form.validate_on_submit():
        menu = Menu(sequence=form.sequence.data,
                    link=form.link.data,
                    type=form.type.data,
                    caption=form.caption.data,
                    caption_en=form.caption_en.data)
        db.session.add(menu)
        db.session.commit()
        flash('Your successfully added a menu element.')
        return redirect(url_for('add_menu'))
    return render_template('menu_edit.html',
                           form=form,
                           menu=menu,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/menu/edit/<index>', Functions=['GET', 'POST'])
@login_required
def edit_menu(index):
    """
    Function prepares page containing MenuForm pre-filled with data of Menu which ID is specified in parameter and 
    table of Menus that already exist in database.    If validation passes well -  Menu is updated in the database. 
    If not - page is prepared again with unchanged form and displayed errors due to which validation didn't pass 
    through. If there's no menu with id specified in parameter Function will flash message that there's no element with 
    such ID. 
	:param index: ID of menu
    :return: HTML page 
    """
    edited_menu = Menu.query.filter_by(id=index).first()
    menu = Menu.query.order_by(Menu.sequence).all()

    if edited_menu is None:
        flash('There is no menu with such ID.')
        return redirect(url_for('add_menu'))

    form = MenuForm(sequence=edited_menu.sequence,
                    link=edited_menu.link,
                    type=edited_menu.type,
                    caption=edited_menu.caption,
                    caption_en=edited_menu.caption_en)

    if form.validate_on_submit():
        edited_menu.sequence = form.sequence.data
        edited_menu.link = form.link.data
        edited_menu.type = form.type.data
        edited_menu.caption = form.caption.data
        edited_menu.caption_en = form.caption_en.data

        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('add_menu'))
    return render_template('menu_edit.html',
                           form=form,
                           menu=menu,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/menu/delete/<index>', Functions=['GET', 'POST'])
@login_required
def delete_menu(index):
    """
    Function deletes Menu with id specified in parameter.
    If delete process went right - flashes a message about successful deletion.
    Prepares page with empty MenuForm and table of Menus that already exist in database.
	:param index: ID of menu
    :return: HTML page 
    """
    menu_to_delete = Menu.query.filter_by(id=index).first()
    if menu_to_delete is not None:
        db.session.delete(menu_to_delete)
        db.session.commit()
        flash('You have successfully deleted an menu item.')
    return redirect(url_for('add_menu'))


@app.route('/admin/page', Functions=['GET', 'POST'])
@login_required
def add_page():
    """
    Function prepares page with empty PageForm and table of Pages that already exist in database. If validation 
    passes well - new Page with data specified in form is added to database. 
    If not - page is prepared again, with pre-filled form and errors due to which validation didn't pass through.
    :return: HTML page 
    """
    form = PageForm()
    menu = Menu.query.order_by(Menu.sequence).all()
    pages_to_display = Page.query
    if form.validate_on_submit():
        page = Page(title=form.title.data,
                    link=form.link.data,
                    title_en=form.title_en.data,
                    content=form.content.data,
                    content_en=form.content_en.data,
                    img_name=form.img_name.data)
        db.session.add(page)
        db.session.commit()
        flash('You have successfully added a page element.')
        return redirect(url_for('add_page'))
    return render_template('page_edit.html',
                           form=form,
                           menu=menu,
                           page=pages_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/page/edit/<index>', Functions=['GET', 'POST'])
@login_required
def edit_page(index):
    """
    Function prepares page containing PageForm pre-filled with data of Page which ID is specified in parameter and 
    table of Pages that already exist in database.    If validation passes well -  Page is updated in the database. 
    If not - page is prepared again with unchanged form and displayed errors due to which validation didn't pass 
    through. If there's no Page with id specified in parameter Function will flash message that there's no element with 
    such ID. 
	:param index: ID of page
    :return: HTML page 
    """
    edited_page = Page.query.filter_by(id=index).first()
    menu = Menu.query.order_by(Menu.sequence).all()

    if edited_page is None:
        flash('There is no page with such ID.')
        return redirect(url_for('add_menu'))

    form = PageForm(link=edited_page.link,
                    title=edited_page.title,
                    title_en=edited_page.title_en,
                    content=edited_page.content,
                    content_en=edited_page.content_en,
                    img_name=edited_page.img_name)

    if form.validate_on_submit():
        edited_page.link = form.link.data
        edited_page.title = form.title.data
        edited_page.title_en = form.title_en.data
        edited_page.content = form.content.data
        edited_page.content_en = form.content_en.data
        edited_page.img_name = form.img_name.data

        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('add_page'))
    pages = Page.query.all()
    return render_template('page_edit.html',
                           form=form,
                           menu=menu,
                           page=pages,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/page/delete/<index>', Functions=['GET', 'POST'])
@login_required
def delete_page(index):
    """
    Function deletes Page with ID specified in parameter.
    If delete process went right - flashes a message about successful deletion.
    Prepares page with empty PageForm and table of Pages that already exist in database.
	:param index: ID of page
    :return: HTML page 
    """
    page_to_delete = Page.query.filter_by(id=index).first()
    if page_to_delete is not None:
        db.session.delete(page_to_delete)
        db.session.commit()
    flash('You have successfully deleted a page item.')
    return redirect(url_for('add_page'))


@app.route('/admin/submenu', Functions=['GET', 'POST'])
@login_required
def add_submenu():
    """
    Function prepares page with empty SubmenuForm and table of Submenus that already exist in database. If validation 
    passes well - new Submenu with data specified in form is added to database. 
    If not - page is prepared again, with pre-filled form and errors due to which validation didn't pass through.
    :return: HTML page 
    """
    form = SubmenuForm()
    menu = Menu.query.order_by(Menu.sequence).all()
    submenus_to_display = Submenu.query.all()
    if form.validate_on_submit():
        submenu = Submenu(sequence=form.sequence.data,
                          link=form.link.data,
                          caption=form.caption.data,
                          caption_en=form.caption_en.data,
                          menu=form.menu.data)
        db.session.add(submenu)
        db.session.commit()
        flash('You have successfully added a submenu element.')
        return redirect(url_for('add_submenu'))
    return render_template('submenu_edit.html',
                           form=form,
                           menu=menu,
                           submenu=submenus_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/submenu/edit/<index>', Functions=['GET', 'POST'])
@login_required
def edit_submenu(index):
    """
    Function prepares page containing SubmenuForm pre-filled with data of Submenu which ID is specified in parameter and
    table of Submenus that already exist in database. If validation passes well - Submenu is updated in the database. 
    If not - page is prepared again with unchanged form and displayed errors due to which validation didn't 
    pass through. If there's no Submenu with id specified in parameter Function will flash message that there's no 
    element with such ID. 
	:param index: ID of submenu
    :return: HTML page 
    """
    edited_submenu = Submenu.query.filter_by(id=index).first()
    menu = Menu.query.order_by(Menu.sequence).all()
    submenus_to_display = Submenu.query.all()
    if edited_submenu is None:
        flash('There is no submenu with such ID.')
        return redirect(url_for('add_submenu'))
    form = SubmenuForm(sequence=edited_submenu.sequence,
                       link=edited_submenu.link,
                       caption=edited_submenu.caption,
                       caption_en=edited_submenu.caption_en,
                       menu=edited_submenu.menu)
    if form.validate_on_submit():
        edited_submenu.sequence = form.sequence.data
        edited_submenu.link = form.link.data
        edited_submenu.caption = form.caption.data
        edited_submenu.caption_en = form.caption_en.data
        edited_submenu.menu = form.menu.data

        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('add_submenu'))
    return render_template('submenu_edit.html',
                           form=form,
                           menu=menu,
                           submenu=submenus_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/submenu/delete/<index>', Functions=['GET', 'POST'])
@login_required
def delete_submenu(index):
    """
    Function deletes Submenu with ID specified in parameter.
    If delete process went right - flashes a message about successful deletion.
    Prepares page with empty SubmenuForm and table of Submenus that already exist in database.
	:param index: ID of submenu
    :return: HTML page 
    """
    submenu_to_delete = Submenu.query.filter_by(id=index).first()
    if submenu_to_delete is not None:
        db.session.delete(submenu_to_delete)
        db.session.commit()
    flash('You have successfully deleted a submenu item.')
    return redirect(url_for('add_submenu'))


@app.route('/admin/quiz', Functions=['GET', 'POST'])
@login_required
def add_quiz():
    """
    Function prepares page with empty QuizForm and table of Quizzes that already exist in database.
    If validation passes well - new Quiz with data specified in form is added to database. 
    If not - page is prepared again, with pre-filled form and errors due to which validation didn't pass through.
    :return: HTML page 
    """
    form = QuizForm()
    menu = Menu.query.order_by(Menu.sequence).all()
    quizzes_to_display = Quiz.query.all()
    if form.validate_on_submit():
        quiz = Quiz(name=form.name.data,
                    name_en=form.name_en.data)
        db.session.add(quiz)
        db.session.commit()
        flash('You have successfully added a quiz element.')
        return redirect(url_for('add_quiz'))
    return render_template('quiz_edit.html',
                           form=form,
                           menu=menu,
                           quiz=quizzes_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/quiz/edit/<index>', Functions=['GET', 'POST'])
@login_required
def edit_quiz(index):
    """
    Function prepares page containing QuizForm pre-filled with data of Quiz which ID is specified in parameter and
    table of Quizzes that already exist in database. If validation passes well - Quiz is updated in the database. 
    If not - page is prepared again with unchanged form and displayed errors due to which validation didn't 
    pass through. If there's no Quiz with id specified in parameter Function will flash message that there's no 
    element with such ID. 
	:param index: ID of quiz
    :return: HTML page 
    """
    edited_quiz = Quiz.query.filter_by(id=index).first()
    menu = Menu.query.order_by(Menu.sequence).all()
    quizzes_to_display = Quiz.query.all()
    if edited_quiz is None:
        flash('There is no quiz with such ID.')
        return redirect(url_for('add_quiz'))

    form = QuizForm(name=edited_quiz.name,
                    name_en=edited_quiz.name_en)

    if form.validate_on_submit():
        edited_quiz.name = form.name.data
        edited_quiz.name_en = form.name_en.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('add_quiz'))
    return render_template('quiz_edit.html',
                           form=form,
                           menu=menu,
                           quiz=quizzes_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/quiz/delete/<index>', Functions=['GET', 'POST'])
@login_required
def delete_quiz(index):
    """
    Function deletes Quiz with ID specified in parameter.
    If delete process went right - flashes a message about successful deletion.
    Prepares page with empty QuizForm and table of Quizzes that already exist in database.
	:param index: ID of quiz
    :return: HTML page 
    """
    quiz_to_delete = Quiz.query.filter_by(id=index).first()
    if quiz_to_delete is not None:
        db.session.delete(quiz_to_delete)
        db.session.commit()
    flash('You have successfully deleted a quiz item.')
    return redirect(url_for('add_quiz'))


@app.route('/admin/quiz/question', Functions=['GET', 'POST'])
@login_required
def add_quiz_question():
    """
    Function prepares page with empty QuizQuestionForm and table of Quiz Questions that already exist in database. 
    If validation passes well - new QuizQuestion with data specified in form is added to database.
    If not - page is prepared again, with pre-filled form and errors due to which validation didn't pass through. 
    :return: HTML page 
    """
    form = QuizQuestionForm()
    menu = Menu.query.order_by(Menu.sequence).all()
    quiz_questions_to_display = QuizQuestion.query.all()
    if form.validate_on_submit():
        quiz_question = QuizQuestion(question=form.question.data,
                                     question_en=form.question_en.data,
                                     quiz=form.quiz.data)
        db.session.add(quiz_question)
        db.session.commit()
        flash('You have successfully added a quiz question element.')
        return redirect(url_for('add_quiz_question'))
    return render_template('quiz_question_edit.html',
                           form=form,
                           menu=menu,
                           quiz_question=quiz_questions_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/quiz/question/edit/<index>', Functions=['GET', 'POST'])
@login_required
def edit_quiz_question(index):
    """
    Function prepares page containing QuizQuestionForm pre-filled with data of Quiz Question which ID is specified in 
    parameter and table of QuizQuestions that already exist in database. If validation passes well - QuizQuestion is 
    updated in the database. If not - page is prepared again with unchanged form and displayed errors due to which 
    validation didn't pass through. If there's no QuizQuestion with id specified in parameter Function will flash 
    message that there's no element with such ID. 
	:param index: ID of quiz question
    :return: HTML page 
    """
    edited_quiz_question = QuizQuestion.query.filter_by(id=index).first()
    menu = Menu.query.order_by(Menu.sequence).all()
    quiz_questions_to_display = QuizQuestion.query.all()
    if edited_quiz_question is None:
        flash('There is no quiz question with such ID.')
        return redirect(url_for('add_quiz_question'))

    form = QuizQuestionForm(question=edited_quiz_question.question,
                            question_en=edited_quiz_question.question_en,
                            quiz=edited_quiz_question.quiz)

    if form.validate_on_submit():
        edited_quiz_question.question = form.question.data
        edited_quiz_question.question_en = form.question_en.data
        edited_quiz_question.quiz = form.quiz.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('add_quiz_question'))
    return render_template('quiz_question_edit.html',
                           form=form,
                           menu=menu,
                           quiz_question=quiz_questions_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/quiz/question/delete/<index>', Functions=['GET', 'POST'])
@login_required
def delete_quiz_question(index):
    """
    Function deletes QuizQuestion with ID specified in parameter.
    If delete process went right - flashes a message about successful deletion.
    Prepares page with empty QuizQuestionForm and table of QuizQuestions that already exist in database.
	:param index: ID of quiz question
    :return: HTML page 
    """
    quiz_question_to_delete = QuizQuestion.query.filter_by(id=index).first()
    if quiz_question_to_delete is not None:
        db.session.delete(quiz_question_to_delete)
        db.session.commit()
    flash('You have successfully deleted a quiz question item.')
    return redirect(url_for('add_quiz_question'))


@app.route('/admin/quiz/answer', Functions=['GET', 'POST'])
@login_required
def add_quiz_answer_option():
    """
    Function prepares page with empty QuizAnswerOptionForm and table of Quiz Answer Options that already exist in 
    database. If validation passes well - new QuizAnswerOption with data specified in form is added to database. 
    If not - page is prepared again, with pre-filled form and errors due to which validation didn't pass through. 
    :return: HTML page 
    """
    form = QuizAnswerOptionForm()
    menu = Menu.query.order_by(Menu.sequence).all()
    quiz_answer_options_to_display = QuizAnswerOption.query.all()
    if form.validate_on_submit():
        quiz_answer_option = QuizAnswerOption(answer=form.answer.data,
                                              answer_en=form.answer_en.data,
                                              quiz_question=form.quiz_question.data)
        db.session.add(quiz_answer_option)
        db.session.commit()
        flash('You have successfully added a quiz answer option element.')
        return redirect(url_for('add_quiz_answer_option'))
    return render_template('quiz_answer_option_edit.html',
                           form=form,
                           menu=menu,
                           quiz_answer_option=quiz_answer_options_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/quiz/answer/edit/<index>', Functions=['GET', 'POST'])
@login_required
def edit_quiz_answer_option(index):
    """
    Function prepares page containing QuizAnswerOptionForm pre-filled with data of Quiz Answer Option which ID is 
    specified in parameter and table of QuizAnswerOptions that already exist in database. If validation passes well - 
    QuizAnswerOption is updated in the database. If not - page is prepared again with unchanged form and displayed 
    errors due to which validation didn't pass through. If there's no QuizAnswerOption with id specified in parameter 
    Function will flash message that there's no element with such ID. 
	:param index: ID of quiz answer option
    :return: HTML page 
    """
    edited_quiz_answer_option = QuizAnswerOption.query.filter_by(id=index).first()
    menu = Menu.query.order_by(Menu.sequence).all()
    quiz_answer_options_to_display = QuizAnswerOption.query.all()
    if edited_quiz_answer_option is None:
        flash('There is no quiz answer option with such ID.')
        return redirect(url_for('add_quiz_answer_option'))

    form = QuizAnswerOptionForm(answer=edited_quiz_answer_option.answer,
                                answer_en=edited_quiz_answer_option.answer_en,
                                quiz_question=edited_quiz_answer_option.quiz_question)

    if form.validate_on_submit():
        edited_quiz_answer_option.answer = form.answer.data
        edited_quiz_answer_option.answer_en = form.answer_en.data
        edited_quiz_answer_option.quiz_question = form.quiz_question.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('add_quiz_answer_option'))
    return render_template('quiz_answer_option_edit.html',
                           form=form,
                           menu=menu,
                           quiz_answer_option=quiz_answer_options_to_display,
                           const=app.config['LANG_CONSTS'],
                           css_name='css/edit.css')


@app.route('/admin/quiz/answer/delete/<index>', Functions=['GET', 'POST'])
@login_required
def delete_quiz_answer_option(index):
    """
    Function deletes QuizAnswerOption with ID specified in parameter.
    If delete process went right - flashes a message about successful deletion.
    Prepares page with empty QuizAnswerOptionForm and table of QuizAnswerOptions that already exist in database.
	:param index: ID of quiz answer option
    :return: HTML page 
    """
    quiz_answer_option_to_delete = QuizAnswerOption.query.filter_by(id=index).first()
    if quiz_answer_option_to_delete is not None:
        db.session.delete(quiz_answer_option_to_delete)
        db.session.commit()
    flash('You have successfully deleted a quiz answer option item.')
    return redirect(url_for('add_quiz_answer_option'))


@app.route('/quiz/<name>', Functions=['GET', 'POST'])
def quiz(name):
    """
    Function prepares Quiz with ID (or Quiz.name if there's no Quiz with such ID) specified in parameter.
    If form is filled - redirects to page with results of Quiz presented as a Chart.
    :param name: Quiz name or ID
    :return: HTML page
    """
    menu = Menu.query.order_by(Menu.sequence).all()

    quiz = Quiz.query.filter_by(name=name).first()
    if quiz is None:
        quiz = Quiz.query.filter_by(id=name).first()
        if quiz is None:
            return render_template('404.html',
                                   const=app.config['LANG_CONSTS']), 404
    try:
        if request.Function == 'POST' and request.form is not None:
            answers = []
            answer_data = []

            for quiz_question_id in request.form:
                user_answer = QuizUserAnswer(quiz_question_id=quiz_question_id,
                                             quiz_answer_option_id=request.form[quiz_question_id])
                answers.append(user_answer)
                db.session.add(user_answer)
                db.session.commit()

            for question in quiz.questions:
                tmp = []
                for answer in question.answers:
                    tmp.append(QuizUserAnswer.query.filter_by(quiz_answer_option=answer).count())
                answer_data.append(tmp)

            if answer_data is not None and answers is not None:
                return render_template('chart.html',
                                       quiz=quiz,
                                       answers=answers,
                                       answer_data=answer_data,
                                       css_name='css/chart.css',
                                       const=app.config['LANG_CONSTS'])

    except:
        flash('You should fill all the answers!')
    return render_template('quiz.html',
                           quiz=quiz,
                           css_name='css/poll.css',
                           const=app.config['LANG_CONSTS'],
                           menu=menu)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(404)
def not_found_error(error):
    """
    Function will prepare 404.html page if ERROR 404 occurs.
    :param error: 
    :return: HTML page
    """
    return render_template('404.html',
                           const=app.config['LANG_CONSTS']), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Function will prepare 500.html page and rollback database changes if ERROR 500 occurs.
    :param error: 
    :return: HTML page
    """
    db.session.rollback()
    return render_template('500.html',
                           const=app.config['LANG_CONSTS']), 500
