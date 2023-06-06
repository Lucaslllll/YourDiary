from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.storage.jsonstore import JsonStore

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.snackbar.snackbar import MDSnackbarActionButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from kaki.app import App


from components.connection import AccessDB

class Register(MDScreen):

    def alert_error_connection(self, text, *args):
        Snackbar(
            MDLabel(
                text=text,
                theme_text_color="Custom",
                text_color="#393231",
            ),
            MDSnackbarActionButton(
                text="close",
                theme_text_color="Custom",
                text_color="#8E353C",
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            md_bg_color="#E8D8D7",
        ).open()
        

    def do_register(self, *args):
        data = {
            "username": self.ids.id_text_username.text,
            "first_name": self.ids.id_text_first.text,
            "last_name": self.ids.id_text_last.text,
            "email": self.ids.id_text_email.text,
            "password": self.ids.id_text_password.text,
            "terms_of_use": self.ids.id_text_terms_of_use.active

        }

        user = AccessDB(name_url="accounts/users/", tag="USERS")
        resposta = user.post(data=data)
        
        if resposta == True:
            self.pass_of_register()
        elif not self.ids.id_text_terms_of_use.active:
            self.alert_error_connection(text="marque os termos de uso")
        elif type(resposta) is dict:
            self.pass_of_register()
        else:
            self.alert_error_connection(text=resposta)


    def pass_of_register(self, *args):
        self.manager.current = "login_name"

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)


    def voltar_android(self, *args, **kwargs):
        self.manager.current = "login_name"
        return True

    def voltar(self, window, key, *args):
        if key == 27:
            self.manager.current = "login_name"
            return True

        return False

    def timeout_spinner(self, *args):
        self.ids.load_spinner.active = False
      
    def on_press_spinner(self, *args):
        self.ids.load_spinner.active = True
        self.ids.load_spinner.determinate = False
        self.ids.load_spinner.determinate_time = 2
        Clock.schedule_once(self.timeout_spinner, 3)