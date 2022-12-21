from kivy.uix.screenmanager import ScreenManager
from kivy.storage.jsonstore import JsonStore
from kaki.app import App


sm = ScreenManager()

class MainScreenManager(ScreenManager):
    path = ""
    user_id = None
    current_view_annotation = None
    background_annotation = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = App.get_running_app().user_data_dir+"/"
        
        
            
        store = JsonStore(self.path+"data.json")
        if store.exists('login_auth'):
            if store.get('login_auth')['access'] == True:
                # self.current = "diary_name"
                self.user_id = store.get("user")["id"]
                