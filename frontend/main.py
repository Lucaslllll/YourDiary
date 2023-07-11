# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory

from components.authentication import Authenticat
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

from kivy.core.window import Window
from kivy.config import Config
Window.softinput_mode = 'below_target'
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('kivy', 'exit_on_escape', 'False')

# para imagens https funcionarem
import os
import certifi
import ssl
ssl.get_default_verify_paths()
os.environ['SSL_CERT_FILE'] = "/etc/letsencrypt/live/yourdiary.top/fullchain.pem"


# linux package
from kivymd import hooks_path as kivymd_hooks_path


class YourDiaryApp(App, MDApp):
    def __init__(self, **kwargs):
        # herdará de buttonbehavior e label
        super(YourDiaryApp, self).__init__(**kwargs)
        self.path = self.user_data_dir+"/"
        self.auth = Authenticat()
        self.resposta = self.auth.do_auth()
        self.token_access = self.auth.get_token()
        self.token_refresh = self.auth.get_token_refresh()

        if self.resposta == True:
            store = JsonStore(self.path+'data.json')
            store.put('authentication',
                    resposta=self.resposta,
                    token_access=self.token_access,
                    token_refresh=self.token_refresh
                )
        Clock.schedule_interval(self.reload, 120)


    # apenas na produção, lembrar de tira quando for compilar
    DEBUG = 1

    KV_FILES = {
        os.path.join(os.getcwd(), "screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "screens/login_screen/login.kv"),
        os.path.join(os.getcwd(), "screens/register_screen/register.kv"),
        os.path.join(os.getcwd(), "screens/diary_screen/diary.kv"),
        os.path.join(os.getcwd(), "screens/diary_list_screen/diary-list.kv"),
        os.path.join(os.getcwd(), "screens/diary_edit_screen/diary-edit.kv"),
        os.path.join(os.getcwd(), "screens/annotation_screen/annotation.kv"),
        os.path.join(os.getcwd(), "screens/chat_screen/chat.kv"),
        os.path.join(os.getcwd(), "screens/chat_list_screen/chat-list.kv"),
        os.path.join(os.getcwd(), "screens/profile_screen/profile.kv"),
        os.path.join(os.getcwd(), "screens/about_screen/about.kv"),
        os.path.join(os.getcwd(), "screens/splash_screen/splash.kv"),
        os.path.join(os.getcwd(), "screens/hero_screen/hero.kv"),
        os.path.join(os.getcwd(), "screens/configuration_screen/configuration.kv"),
        os.path.join(os.getcwd(), "screens/image_add_screen/image-add.kv"),
        os.path.join(os.getcwd(), "screens/search_screen/search.kv"),


    }


    CLASSES = {
        "MainScreenManager": "screens.screenmanager",
        "Login": "screens.login_screen.login",
        "Register": "screens.register_screen.register",
        "Diary": "screens.diary_screen.diary",
        "DiaryEdit": "screens.diary_edit_screen.diary-edit",
        "DiaryList": "screens.diary_list_screen.diary-list",
        "Annotation": "screens.annotation_screen.annotation",
        "Chat": "screens.chat_screen.chat",
        "ChatList": "screens.chat_list_screen.chat-list",
        "Profile": "screens.profile_screen.profile",
        "About": "screens.about_screen.about",
        "Splash": "screens.splash_screen.splash",
        "Hero": "screens.hero_screen.hero",
        "Configuration": "screens.configuration_screen.configuration",
        "ImageAdd": "screens.image_add_screen.image-add",
        "Search": "screens.search_screen.search",

    }


    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def reload(self, *args):
        self.resposta = self.auth.do_auth()
        self.token_access = self.auth.get_token()
        self.token_refresh = self.auth.get_token_refresh()
        store = JsonStore(self.path+'data.json')
        store.put('authentication',
                    resposta=self.resposta,
                    token_access=self.token_access,
                    token_refresh=self.token_refresh
                )

    def build_app(self):
        return Factory.MainScreenManager()

YourDiaryApp().run()
