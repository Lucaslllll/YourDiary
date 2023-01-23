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
from kivymd.uix.filemanager import MDFileManager

from kaki.app import App
from components.connection import AccessDB
import os
from kivy.utils import platform
from kivymd.toast import toast


class Profile(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        self.user_db = AccessDB(name_url="accounts/users", tag="USERS")
        self.profile_followers = ""
        self.profile_following = ""
        

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)
        self.files = {}
        self.texto_alert = ""
        Clock.schedule_once(self.on_start, 1)
       

    def on_start(self, *args):
        if self.manager.current_view_user == self.manager.user_id:
            self.user_ob = self.user_db.get(id_object=self.manager.user_id)
            self.ids.idImageProfile.disabled = False
            
            self.ids.idValidationEmail.opacity = 1
            self.ids.idValidationEmail.disabled = False
 
            self.ids.idButtonConfig.disabled = False
            self.ids.idButtonConfig.opacity = 1
            self.ids.idButtonChat.disabled = True
            self.ids.idButtonChat.opacity = 0
            self.ids.idButtonFollow.disabled = True
            self.ids.idButtonFollow.opacity = 0

            # print("if " +str(self.manager.current_view_user))

        else:
            self.user_ob = self.user_db.get(id_object=self.manager.current_view_user)
            self.ids.idImageProfile.disabled = True

            self.ids.idButtonConfig.disabled = True
            self.ids.idButtonConfig.opacity = 0
            self.ids.idButtonChat.disabled = False
            self.ids.idButtonChat.opacity = 1
            self.ids.idButtonFollow.disabled = False
            self.ids.idButtonFollow.opacity = 1
            
            # print("else " +str(self.manager.current_view_user))

        


        if type(self.user_ob) is dict:
            if self.user_ob["image"] != None:
                self.ids.idImageProfile.source = self.user_ob["image"]

            self.ids.idNamePerfil.text = "".join([self.user_ob["first_name"], " ", self.user_ob["last_name"] ]) 

            profile_ob =  AccessDB(name_url="accounts/profiles/check", tag="PROFILES")
            profile_ob = profile_ob.get(id_object=self.manager.current_view_user)

            if len(profile_ob) != 0:
                if self.manager.user_id in profile_ob[0]["followers"]:
                    # self.ids.idButtonFollow.disabled = True
                    self.ids.idButtonFollow.icon = "account-check"
                    self.ids.idButtonFollow.on_release = self.do_unfollow
                else:
                    self.ids.idButtonFollow.on_release = self.do_follow    

                self.ids.idFollowerLabel.text = "".join([str(len(profile_ob[0]["followers"])), " Seguidores"])
                self.ids.idFollowingLabel.text = "".join([ str(len(profile_ob[0]["following"])), " Seguindo"])                

            else:
                self.ids.idButtonFollow.on_release = self.do_follow
            

            
            

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)
        self.ids.idButtonProfile.opacity = 0
        self.ids.idButtonProfile.disabled = True

        self.ids.idValidationEmail.opacity = 0
        self.ids.idValidationEmail.disabled = True        

        self.ids.idButtonConfig.opacity = 0
        self.ids.idButtonConfig.disabled = True
        self.ids.idButtonChat.opacity = 0
        self.ids.idButtonChat.disabled = True
        self.ids.idButtonFollow.opacity = 0
        self.ids.idButtonFollow.disabled = True



    # part of form annotation
    def file_manager_open(self):
        if platform != 'android' :
            self.file_manager.show(os.path.expanduser("~"))
            self.manager_open = True

        else:
            import android
            from android.storage import primary_external_storage_path
            from android.permissions import request_permissions, Permission
            
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            ext_path = primary_external_storage_path()

            print(ext_path)
            self.file_manager.show(ext_path)
            self.manager_open = True  

    def select_path(self, path: str):
        self.exit_manager()
        self.files = {'image': open(path, 'rb')}
        toast(path)


    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
        self.ids.idButtonProfile.opacity = 50
        self.ids.idButtonProfile.disabled = False



    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()

        return True


    def send_photo(self):
        
        user_ob = self.user_db.patch(id_object=self.manager.user_id, data={}, files=self.files)

        if type(user_ob) is dict:
            self.manager.current = "diary_name"
        else:
            self.texto_alert = "Erro: Imagens Acima de 8mb ou Formato Inválido"
            Clock.schedule_once(self.alert_error_connection, 2)


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

    def timeout_spinner(self, *args):
        self.ids.load_spinner_note.active = False
      
    def on_press_spinner(self, *args):
        self.ids.load_spinner_note.active = True
        self.ids.load_spinner_note.determinate = False
        self.ids.load_spinner_note.determinate_time = 2
        # depois de 3 segundos executará timeout_spinner
        # desligando o spinner
        Clock.schedule_once(self.timeout_spinner, 3)


    def go_chat(self):
        self.manager.user_id_chat = self.manager.current_view_user
        self.manager.current = "chat_name"

    def do_follow(self):
        data = {
            "user": self.manager.current_view_user,
            "followers": [self.manager.user_id]
        }

        dataUser = {
            "user": self.manager.user_id,
            "following": [self.manager.current_view_user]
        }

        profile_ob =  AccessDB(name_url="accounts/profiles/check", tag="PROFILES")
        profile_ob = profile_ob.get(id_object=self.manager.current_view_user)

        if len(profile_ob) == 0:
            profile_ob =  AccessDB(name_url="accounts/profiles/", tag="PROFILES")
            profile_ob = profile_ob.post(data=data)

        else:   
            followers = profile_ob[0]["followers"]
            data["followers"] = list(set(followers) | set(data["followers"]))
            
            profile_ob =  AccessDB(name_url="accounts/profiles", tag="PROFILES")
            profile_ob = profile_ob.patch(id_object=self.manager.current_view_user, data=data)
        
        self.update_profiles(unfollow=False)

            


        profile_user_ob =  AccessDB(name_url="accounts/profiles/check", tag="PROFILES")
        profile_user_ob = profile_user_ob.get(id_object=self.manager.user_id)
        
        if len(profile_user_ob) == 0:
            profile_user_ob =  AccessDB(name_url="accounts/profiles/", tag="PROFILES")
            profile_user_ob = profile_user_ob.post(data=dataUser)

        else:
            following = profile_user_ob[0]["following"]
            dataUser["following"] = list(set(following) | set(dataUser["following"]))

            profile_user_ob =  AccessDB(name_url="accounts/profiles", tag="PROFILES")
            profile_user_ob = profile_user_ob.patch(id_object=self.manager.user_id, data=dataUser)
            




    def do_unfollow(self):
        profile_ob =  AccessDB(name_url="accounts/profiles/check", tag="PROFILES")
        profile_ob = profile_ob.get(id_object=self.manager.current_view_user)
        if len(profile_ob) != 0:
            
            if self.manager.user_id in profile_ob[0]["followers"]:
                profile_ob[0]["followers"].remove(self.manager.user_id)
                data = profile_ob[0]
                profile_ob =  AccessDB(name_url="accounts/profiles", tag="PROFILES")
                profile_ob = profile_ob.put(id_object=self.manager.current_view_user, data=data)

            

        profile_user_ob =  AccessDB(name_url="accounts/profiles/check", tag="PROFILES")
        profile_user_ob = profile_user_ob.get(id_object=self.manager.user_id)        
        if len(profile_user_ob) != 0:
            
            if self.manager.current_view_user in profile_user_ob[0]["following"]:
                profile_user_ob[0]["following"].remove(self.manager.current_view_user)
                data = profile_user_ob[0]
                print(data)
                profile_user_ob =  AccessDB(name_url="accounts/profiles", tag="PROFILES")
                profile_user_ob = profile_user_ob.put(id_object=self.manager.user_id, data=data)
                self.update_profiles(unfollow=True)            




    def update_profiles(self, unfollow):
        if unfollow:
            self.ids.idButtonFollow.icon = "account-arrow-left"
            self.ids.idButtonFollow.on_release = self.do_follow
        else:
            self.ids.idButtonFollow.icon = "account-check"
            self.ids.idButtonFollow.on_release = self.do_unfollow

        profile_ob =  AccessDB(name_url="accounts/profiles/check", tag="PROFILES")
        profile_ob = profile_ob.get(id_object=self.manager.current_view_user)        
        self.ids.idFollowerLabel.text = "".join([str(len(profile_ob[0]["followers"])), " Seguidores"])
        self.ids.idFollowingLabel.text = "".join([ str(len(profile_ob[0]["following"])), " Seguindo"])




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

