from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.storage.jsonstore import JsonStore

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip

from kaki.app import App
from datetime import datetime
from components.connection import AccessDB



class About(MDScreen):
    def __init__(self, **kwargs):
        super(About, self).__init__(**kwargs)
        self.texto_alert = None
        self.about_1 = "O intuito é criar um espaço para anotações como na forma de um diário digital "\
                       "que pode ser pessoal ou compartilhado globalmente com outras pessoas. "\
                       "Eu acredito que poderá ser usado para desabafar, colocar as situações "\
                       "do dia a dia aqui ou talvez até servir como uma terapia para angustias e coisas " \
                       "que não podemos falar para qualquer um, seja por ser besta demais para incomodar terceiros "\
                       "ou por ser íntimo demais, até para os mais próximos. "\
                       "O app ainda está na versão beta e eu pretendo ir melhorando com as sugestões, que vocês usuários, "\
                       "me mandarem. O app tentará focar no anonimato do usuário, mas caso eu tenha problemas em relação "\
                       "a isso, irei repensar, espero que alguém consiga fazer bom proveito dessa ideia. \n\n lembre-se: O que é pessoal somente você poderá ler, "\
                       "mas o que está público outras pessoas poderão também ler ;)"                      



    def on_pre_enter(self):
        Window.bind(on_request_close=self.voltar_android)
        Window.bind(on_keyboard=self.voltar)

    def on_pre_leave(self):
        Window.unbind(on_request_close=self.voltar_android)
        Window.unbind(on_keyboard=self.voltar)


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
        snackbar = Snackbar(
                text=self.texto_alert,
                snackbar_x="10dp",
                snackbar_y="10dp",
                buttons=[
                    MDFlatButton(text="Fechar", text_color=(1, 1, 1, 1),
                                theme_text_color='Custom')
                ]
            )
        snackbar.size_hint_x = (
            Window.width - (snackbar.snackbar_x * 2)
        ) / Window.width
        snackbar.open()

    def clear_form(self):
        self.ids.id_titulo_report.text = ""
        self.ids.id_detalhes_report.text = ""



    def voltar_android(self, *args, **kwargs):
        self.manager.current = "diary_name"
        return True

    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            self.manager.current = "diary_name"
            # print(self.manager.current)
            return True

        return False