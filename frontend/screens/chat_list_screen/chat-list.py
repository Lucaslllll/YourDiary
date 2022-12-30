from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import sp
from kivy.uix.label import Label

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget

from kaki.app import App
from datetime import datetime
from components.connection import AccessDB


class ChatList(MDScreen):
    
    def on_pre_enter(self):
        Window.bind(on_request_close=self.voltar_android)
        Window.bind(on_keyboard=self.voltar)
        Clock.schedule_once(self.run_list_fake, 1)


    def on_pre_leave(self):
        Window.unbind(on_request_close=self.voltar_android)
        Window.unbind(on_keyboard=self.voltar)

    def run_list_fake(self, *args):
        for i in range(0, 10):
            self.fake_list_msgs()

    def fake_list_msgs(self):
        self.ids.idlist.add_widget(

            OneLineAvatarListItem(
                ImageLeftWidget(
                    source="assets/imagens/yourdiary-logo.png"
                ),
                text="Single-line item with avatar",
            )
        )

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