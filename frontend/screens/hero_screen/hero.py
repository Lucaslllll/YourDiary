from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.hero import MDHeroFrom
from kivymd.uix.relativelayout import MDRelativeLayout


from typing import Union
from kaki.app import App
from components.connection import AccessDB



class Hero(MDScreen):

    def on_pre_enter(self):
        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')
        store.put('colors', color_main="#a64dff")

        Clock.schedule_once(self.on_start, 1)
        
    
    def go_splash(self):
        store = JsonStore(self.path+'data.json')
        store.put('times', first_time=True)   
        
        self.manager.current = "login_name"

    def on_start(self, *args):
        colorpicker = PopupColor(diary_screen=self)
        self.ids.idChangeColor.add_widget(colorpicker)
        

    

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



class PopupColor(Popup):
    diary_screen = ObjectProperty()
    color = StringProperty()


    def on_pre_enter(self):
        self.ids.picker.bind(color=self.on_color)


    def on_press_dismiss(self, *args):
        self.dismiss()
        self.color = str(self.ids.picker.hex_color)[1:]


        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')
        store.put('colors', color_main=self.color)

        self.diary_screen.manager.color_main = self.color


    def on_color(self, instance, value):
        # print("RGBA = ", str(value))
        # print("HSV = ", str(instance.hsv))
        # print("HEX = ", str(instance.hex_color))
        self.diary_screen.ids.idScreen3.md_bg_color = value
        self.background_color =  value