from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup

from kivymd.uix.screen import MDScreen
from kivymd.uix.hero import MDHeroFrom
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.pickers import MDColorPicker

from typing import Union
from kaki.app import App
from components.connection import AccessDB



class Hero(MDScreen):

    def on_pre_enter(self):
        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')
        store.put('colors', color_main="#ff8080")
    
    def go_splash(self):
        store = JsonStore(self.path+'data.json')
        store.put('times', first_time=True)   
        
        self.manager.current = "login_name"

    def open_color_picker(self):
        self.color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        self.color_picker.open()
        self.color_picker.bind(
            on_select_color=self.on_select_color,
            on_release=self.get_selected_color
        )

    def update_color(self, color: list) -> None:
        store = JsonStore(self.path+'data.json')
        store.put('colors', color_main=color)

        self.manager.color_main = color


    def get_selected_color(
        self,
        instance_color_picker: MDColorPicker,
        type_color: str,
        selected_color: Union[list, str],
    ):
        '''Return selected color.'''

        self.update_color(selected_color[:-1] + [1])

        Popup.dismiss(self.color_picker)


    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''Called when a gradient image is clicked.'''
        
        



# testar para ver se esse custom hero está otimizado
class CustomHero(MDHeroFrom):
    def on_transform_in(
        self, instance_hero_widget: MDRelativeLayout, duration: float
    ):

        Animation(
            radius=[12, 24, 12, 24],
            duration=duration,
            md_bg_color=(0, 1, 1, 1),
        ).start(instance_hero_widget)

    def on_transform_out(
        self, instance_hero_widget: MDRelativeLayout, duration: float
    ):
        '''Called when the hero back from screen **B** to screen **A**.'''

        Animation(
            radius=[24, 12, 24, 12],
            duration=duration,
            md_bg_color=get_color_from_hex(utils.hex_colormap["blue"]),
        ).start(instance_hero_widget)