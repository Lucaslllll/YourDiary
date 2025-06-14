from kivy.core.window import Window
from kivy.clock import Clock

from kivymd.uix.snackbar import Snackbar
from kivymd.uix.snackbar.snackbar import MDSnackbarActionButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen

from kaki.app import App
from components.connection import AccessDB
# from kivy.base import EventLoop
from kivy.core.window import Window




class About(MDScreen):
    def __init__(self, **kwargs):
        super(About, self).__init__(**kwargs)
        self.texto_alert = None
        self.about_1 = "The intention is to create a space for notes as in the form of a digital diary "\
                       "which can be personal or shared globally with other people. "\
                       "I believe it can be used to put poetry, poems, stories, tales, reports, narratives, wishlist, to vent or even the situations "\
                       "of everyday life here or maybe even serve as a therapy for anxieties and things " \
                       "that we can't tell anyone, either because it's too much of a beast to bother others "\
                       "Or for being too intimate, even for those closest to you. " \
                       "The app is still in beta and I intend to improve with the suggestions, that you users, "\
                       "Send me. The app will try to focus on the anonymity of the user, but in case I have problems regarding "\
                       "To that, I'm going to rethink, I hope someone can make good use of this idea. \n\n remember: What is personal only you can read, "\
                       "But what is public other people will also be able to read ;)"



    def on_pre_enter(self):
        Window.bind(on_keyboard=self.on_key)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.on_key)


    def send_report(self):
        data = {
            "annotation": None,
            "author": self.manager.user_id,
            "title": self.ids.id_titulo_report.text,
            "details": self.ids.id_detalhes_report.text,
        }

        annotation = AccessDB(name_url="reports/", tag="ANNOTATIONS")
        resposta = annotation.post(data=data)

        if resposta:
            self.clear_form()
            self.texto_alert = "Enviado Com Sucesso!"
            Clock.schedule_once(self.alert_error_connection, 3)
        else:
            self.texto_alert = resposta
            Clock.schedule_once(self.alert_error_connection, 3)

    def alert_error_connection(self, *args):
        Snackbar(
            MDLabel(
                text=self.texto_alert,
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

    def clear_form(self):
        self.ids.id_titulo_report.text = ""
        self.ids.id_detalhes_report.text = ""



    def on_key(self, window, key, keycode, *args):
        # esc tem o codigo 27
        if key == 27 or key == 41:
            self.manager.current = "diary_name"
            # print(self.manager.current)
            return True
        return False
