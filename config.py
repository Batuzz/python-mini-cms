# coding=utf-8
import os

"""
Contains main constants of an application.
"""

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

LANG_CONSTS = {
    "pl": {
        # Login stuff
        "login": "Zaloguj się",
        "logout": "Wyloguj się",
        "remember_me": "Zapamiętaj mnie",

        # User
        "your_nickname": "Nazwa użytkownika",
        "user": "Użytkownik",
        "profile": "Profil",
        "permission": "Poziom uprawnień",

        # Titles
        "main_title": "Czy jesteś uzależniony?",
        "login_title": "Zaloguj się!",

        # User dialog
        "edit": "Edytuj",
        "delete": "Usuń",
        "go_back": "Wróć",
        "save_changes": "Zapisz zmiany",
        "save_answers": "Zapisz odpowiedzi",

        # ERRORS
        "error_404": "Błąd 404",
        "error_404_content": "Nie znaleziono pliku.",
        "error_500": "Błąd 500",
        "error_500_content": "Wystąpił niespodziewany błąd.",
        "error_admin_has_been_notified": "Administrator został poinformowany. "
                                         "Przepraszamy za problemy wynikające z tego błędu.",

        # Admin panel: MENU
        "menu_edit": "Edycja menu",
        "menu_sequence": "Kolejność",
        "menu_link": "Link",
        "menu_type": "Typ",
        "menu_caption": "Tytuł",
        "menu_caption_en": "Tytuł angielski",

        # Admin panel: SUBMENU
        "submenu_edit": "Edycja submenu",
        "submenu_sequence": "Kolejność",
        "submenu_link": "Link",
        "submenu_caption": "Tytuł",
        "submenu_caption_en": "Tytuł angielski",
        "submenu_menu_selection": "Wybór menu",

        # Admin panel: QUIZ
        "quiz_edit": "Edycja quizów",
        "quiz_name": "Nazwa",
        "quiz_name_en": "Nazwa (wersja angielska)",

        # Admin panel: QUIZ QUESTION
        "quiz_question_edit": "Edycja pytań quizu",
        "quiz_question_content": "Pytanie",
        "quiz_question_content_en": "Pytanie (wersja angielska)",
        "quiz_question_quiz_selection": "Wybór quizu",

        # Admin panel: QUIZ ANSWER
        "quiz_answer_edit": "Edycja odpowiedzi na pytania quizu",
        "quiz_answer_content": "Odpowiedź",
        "quiz_qanswer_content_en": "Odpowiedź (wersja angielska)",
        "quiz_answer_question_selection": "Wybór pytania quizu",

        # Admin panel: PAGE
        "page_edit": "Edycja podstron",
        "page_link": "Link",
        "page_title": "Tytuł",
        "page_title_en": "Tytuł (wersja angielska)",
        "page_content": "Treść",
        "page_content_en": "Treść (wersja angielska)",
        "page_img_name": "Podgląd grafiki",

        # Admin panel
        "admin_panel": "Admin panel",
        "menu": "Menu",
        "page": "Podstrony",
        "submenu": "Podmenu",
        "quiz": "Quiz",
        "quiz_question": "Pytania quizu",
        "quiz_answer": "Odpowiedzi quizu",

        # Other stuff
        "question": "Pytanie",
        "authors": "Autorzy",
        "contact": "Kontakt",
        "slogan": "A czy Ty jesteś uzależniony?",
        "are_you_sure": "Na pewno?",
        "addictions": "Uzależnienia",

        # Chart
        "your_answer": "Twoja odpowiedź",
        "results": "Wyniki"
    },
    "en": {
        # Login stuff
        "login": "Log in",
        "logout": "Log out",
        "remember_me": "Remember me",

        # User
        "your_nickname": "Username",
        "user": "User",
        "profile": "Profile",
        "permission": "Permission level",

        # Titles
        "main_title": "Are you addicted?",
        "login_title": "Log in!",

        # User dialog
        "edit": "Edit",
        "delete": "Delete",
        "go_back": "Go back",
        "save_changes": "Save changes",
        "save_answers": "Save answers",

        # ERRORS
        "error_404": "Error 404",
        "error_404_content": "File not found.",
        "error_500": "Error 500",
        "error_500_content": "Unexpected error occurred.",
        "error_admin_has_been_notified": "System administrator has been notified. "
                                         "We apologize for the problems.",

        # Admin panel: MENU
        "menu_edit": "Edit menu",
        "menu_sequence": "Order",
        "menu_link": "Link",
        "menu_type": "Type",
        "menu_caption": "Title (polish)",
        "menu_caption_en": "Title",

        # Admin panel: SUBMENU
        "submenu_edit": "Submenu edit",
        "submenu_sequence": "Order",
        "submenu_link": "Link",
        "submenu_caption": "Title (polish)",
        "submenu_caption_en": "Title",
        "submenu_menu_selection": "Menu selection",

        # Admin panel: QUIZ
        "quiz_edit": "Quiz edit",
        "quiz_name": "Name (polish)",
        "quiz_name_en": "Name",

        # Admin panel: QUIZ QUESTION
        "quiz_question_edit": "Quiz questions edit",
        "quiz_question_content": "Question (polish)",
        "quiz_question_content_en": "Question",
        "quiz_question_quiz_selection": "Quiz selection",

        # Admin panel: QUIZ ANSWER
        "quiz_answer_edit": "Quiz answers edit",
        "quiz_answer_content": "Answer (polish)",
        "quiz_qanswer_content_en": "Answer",
        "quiz_answer_question_selection": "Question selection",

        # Admin panel: PAGE
        "page_edit": "Pages edit",
        "page_link": "Link",
        "page_title": "Title (polish)",
        "page_title_en": "Title",
        "page_content": "Content (polish)",
        "page_content_en": "Content",
        "page_img_name": "Image",

        # Admin panel
        "admin_panel": "Admin panel",
        "menu": "Menu",
        "page": "Pages",
        "submenu": "Submenu",
        "quiz": "Quiz",
        "quiz_question": "Quiz questions",
        "quiz_answer": "Quiz answers",

        # Other stuff
        "question": "Question",
        "authors": "Authors",
        "contact": "Contact",
        "slogan": "And you, are you addicted?",
        "are_you_sure": "Are you sure?",
        "addictions": "Addictions",

        # Chart
        "your_answer": "Your answer",
        "results": "Results"
    }
}
