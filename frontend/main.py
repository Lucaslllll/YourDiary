# -*- coding: utf-8 -*-

import os

from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory

from kivy.core.window import Window
from kivy.config import Config
Window.softinput_mode = 'below_target'
Config.set('kivy', 'keyboard_mode', 'systemandmulti')


class YourDiaryApp(App, MDApp):

    DEBUG = 1

    KV_FILES = {
        os.path.join(os.getcwd(), "screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "screens/login_screen/login.kv"),
        os.path.join(os.getcwd(), "screens/register_screen/register.kv"),
        os.path.join(os.getcwd(), "screens/diary_screen/diary.kv"),
        os.path.join(os.getcwd(), "screens/diary_list_screen/diary-list.kv"),
        os.path.join(os.getcwd(), "screens/diary_edit_screen/diary-edit.kv"),
        os.path.join(os.getcwd(), "screens/annotation_screen/annotation.kv"),

    }


    CLASSES = {
        "MainScreenManager": "screens.screenmanager",
        "Login": "screens.login_screen.login",
        "Register": "screens.register_screen.register",
        "Diary": "screens.diary_screen.diary",
        "DiaryEdit": "screens.diary_edit_screen.diary-edit",
        "DiaryList": "screens.diary_list_screen.diary-list",
        "Annotation": "screens.annotation_screen.annotation",     

    }


    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def build_app(self):
        return Factory.MainScreenManager()

YourDiaryApp().run()