from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.storage.jsonstore import JsonStore

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelThreeLine
# from kivymd import images_path
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar

from kaki.app import App
from components.connection import AccessDB
import os



class Configuration(MDScreen):

    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)
        
    def on_pre_leave(self):
        self.ids.content.clear_widgets()

    def a(self):
        print("a")

    def on_start(self, *args):
        self.ids.content.add_widget(
                MDExpansionPanel(
                    # icon=os.path.join(images_path, "logo", "kivymd-icon-128.png"),
                    icon="panorama-variant-outline",
                    content=Content("ativar", "claro ou escuro", "arrow-right"),
                    panel_cls=MDExpansionPanelOneLine(
                        text="Background",

                    ),

                )
        )

        self.ids.content.add_widget(
                MDExpansionPanel(
                    # icon=os.path.join(images_path, "logo", "kivymd-icon-128.png"),
                    icon="shield-airplane",
                    content=Content("função não implementada", "usar app offline", "arrow-right"),
                    panel_cls=MDExpansionPanelOneLine(
                        text="Offline",

                    ),

                )
        )

        self.ids.content.add_widget(
            ContentLogout()
        )

    def do_logout(self):
        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')

        if store.exists('login_auth'):
            store.put('login_auth', access=False)

        if store.exists('user'):
            store.put('user', id=None)


        self.manager.current = "login_name"


class Content(BoxLayout):
    first_text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()
    def __init__(self, first_text, secondary_text, icon, **kwargs):
        super(Content, self).__init__(**kwargs)
        self.first_text = first_text
        self.secondary_text = secondary_text
        self.icon = icon

class ContentLogout(BoxLayout):
    pass
