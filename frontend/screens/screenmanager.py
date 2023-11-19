from kivy.uix.screenmanager import ScreenManager
from kaki.app import App


sm = ScreenManager()

class MainScreenManager(ScreenManager):
    path = ""
    user_id = 0
    user_id_chat = 0
    current_view_annotation = 0
    current_view_user = 0
    background_annotation = "None"
    color_main = [.648, .331, 1, 1]
    
