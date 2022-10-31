import os

from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory


class YourDiaryApp(App, MDApp):

    DEBUG = 1

    KV_FILES = {
        os.path.join(os.getcwd(), "screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "screens/login_screen/login.kv"),
    }


    CLASSES = {
        "MainScreenManager": "screens.screenmanager",
        "Login": "screens.login_screen.login",
        

    }
    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def build_app(self):
        return Factory.MainScreenManager()

YourDiaryApp().run()