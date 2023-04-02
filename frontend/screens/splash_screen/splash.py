from kivy.core.window import Window
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kaki.app import App
import os
os.environ['KIVY_IMAGE'] = 'sdl2,gif'

class Splash(MDScreen):

    def __init__(self, **kwargs):
        super(Splash, self).__init__(**kwargs)
        self.path = App.get_running_app().user_data_dir+"/"
        self.store = JsonStore(self.path+'data.json')
        self.current_atual = "login_name"
        
    
    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)
        Clock.schedule_once(self.change_screen, 20)

    def on_start(self, *args):

        if self.store.exists('times'):
            if self.store.get('times')['first_time'] == True:

                if self.store.exists('login_auth'):
                    if self.store.get('login_auth')['access'] == True:
                        self.current_atual = "diary_name"
                        self.manager.user_id = self.store.get("user")["id"]

            else:
                self.current_atual = "hero_name"
        else:
            self.current_atual = "hero_name"

        if self.store.exists('colors'):
            self.manager.color_main = self.store.get('colors')['color_main']
            

    def change_screen(self, *args):
        self.manager.current = self.current_atual