from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.metrics import dp

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelThreeLine
# from kivymd import images_path
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.snackbar.snackbar import MDSnackbarActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers.colorpicker.colorpicker import MDColorPicker
from kivymd.uix.boxlayout import MDBoxLayout


from typing import Union
from kaki.app import App
from components.connection import AccessDB
import os



class Configuration(MDScreen):

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)
        self.path = App.get_running_app().user_data_dir+"/"
        self.texto_alert = ""
        self.step_change_pwrd = 1
        self.user_db = AccessDB(name_url="accounts/users", tag="USERS")
        Clock.schedule_once(self.on_start, 1)

        
    def on_pre_leave(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)
        self.ids.content.clear_widgets()


    def on_start(self, *args):
        self.ids.content.add_widget(
            MDExpansionPanel(
                # icon=os.path.join(images_path, "logo", "kivymd-icon-128.png"),
                icon="lock-reset",
                content=Content(screen=self),
                panel_cls=MDExpansionPanelOneLine(
                    text="Reset Password",

                ),

            )
        )

        # self.ids.content.add_widget(
        #         MDExpansionPanel(
        #             # icon=os.path.join(images_path, "logo", "kivymd-icon-128.png"),
        #             icon="shield-airplane",
        #             content=Content("função não implementada", "usar app offline", "arrow-right"),
        #             panel_cls=MDExpansionPanelOneLine(
        #                 text="Offline",

        #             ),

        #         )
        # )

        self.ids.content.add_widget(
            MDExpansionPanel(
                # icon=os.path.join(images_path, "logo", "kivymd-icon-128.png"),
                icon="format-color-fill",
                content=ContentPickerColor(screen=self),
                panel_cls=MDExpansionPanelOneLine(
                    text="Change Main Color",

                ),

            )
        )

        self.ids.content.add_widget(
            ContentLogout(screen=self)
        )




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






    def steps_to_change(self):
        # passo 1: envio uma mensagem para o email do cara um um código de 6 numeros
        # ele digita corretamente e tem acesso ao passo 2
        # passo 2: ele coloca sua nova senha e consegue mudá-la
        if self.step_change_pwrd == 1:
            self.user_ob = self.user_db.get(id_object=self.manager.user_id)

            if type(self.user_ob) is dict: 
                data = {
                    "email": self.user_ob['email']
                }

                send_email = AccessDB(name_url="accounts/password/redefine/", tag="EMAIL SEND CODE")
                send_email = send_email.post(data=data)

                if type(send_email) is dict:
                    self.texto_alert = "Email Sent Successfully"
                    Clock.schedule_once(self.alert_error_connection, 1)    
                    
                    self.step_change_pwrd = 2
                    self.ids.idButtonSteps.text = "Send Password and Change"
                    self.ids.idButtonSteps.md_bg_color = 0.2, 0.9, 0.7, 1
                    self.ids.idCodeEmail.disabled = False
                    self.ids.idPassword1.disabled = False
                    self.ids.idPassword2.disabled = False

                else:
                    self.texto_alert = "No Connection Or Invalid Email"
                    Clock.schedule_once(self.alert_error_connection, 1)


        elif self.step_change_pwrd == 2:    
            if self.ids.idPassword1.text == self.ids.idPassword2.text and self.ids.idCodeEmail.text != "":
                data = {
                    "username": self.user_ob['username'],
                    "password": self.ids.idPassword1.text

                }

                confirmed = AccessDB(name_url="accounts/password/redefine/confirme", tag="PASSWORD CONFIRME")
                confirmed = confirmed.put(id_object=self.ids.idCodeEmail.text, data=data)

                if type(confirmed) is dict:
                    self.texto_alert = "Password Changed"
                    Clock.schedule_once(self.alert_error_connection, 1)    
                
                    self.step_change_pwrd = 1
                    self.ids.idButtonSteps.text = "Send A Message With Code To Your Email"
                    self.ids.idButtonSteps.md_bg_color = 0.9, 0.7, 0.2, 1
                    self.ids.idCodeEmail.disabled = True
                    self.ids.idPassword1.disabled = True
                    self.ids.idPassword2.disabled = True

                else:
                    self.texto_alert = "No Connection Or Invalid Code"
                    Clock.schedule_once(self.alert_error_connection, 1)

            else:
                self.texto_alert = "Password Not Match"
                Clock.schedule_once(self.alert_error_connection, 1)





    def do_logout(self):
        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')

        if store.exists('login_auth'):
            store.put('login_auth', access=False)

        if store.exists('user'):
            store.put('user', id=None)


        self.manager.current = "login_name"


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


class Content(BoxLayout):
    screen = ObjectProperty()

    def __init__(self, screen, **kwargs):
        super(Content, self).__init__(**kwargs)
        self.screen = screen

        # para manipular os ids de content pela screen
        # é mais interessante e fácil, adicioná-los aos ids da screen 
        screen.ids.idButtonSteps = self.ids.idButtonSteps
        screen.ids.idCodeEmail = self.ids.idCodeEmail
        screen.ids.idPassword1 = self.ids.idPassword1
        screen.ids.idPassword2 = self.ids.idPassword2


class ContentGeneral(BoxLayout):
    first_text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()
    def __init__(self, first_text, secondary_text, icon, **kwargs):
        super(Content, self).__init__(**kwargs)
        self.first_text = first_text
        self.secondary_text = secondary_text
        self.icon = icon




class ContentPickerColor(BoxLayout):
    screen = ObjectProperty()
    color = ListProperty()

    def __init__(self, screen, color=[1, 1, 1, 1], **kwargs):
        super(ContentPickerColor, self).__init__(**kwargs)
        self.screen = screen
        self.color = color


    def on_pre_enter(self):
        self.ids.picker.bind(color=self.on_color)
        

    def on_press_dismiss(self, *args):
        self.ids.popupcolor.dismiss()
        self.color = self.ids.picker.color


        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')
        store.put('colors', color_main=self.color)

        self.screen.manager.color_main = self.color


    def on_color(self, instance, value):
        # colocar na base que background_color necessita
        # background_color não usa o padrão 1, 1, 1, 1 do md_bg_color
        base = 6
        for_background = list(map(lambda x: x * base, value))
        self.ids.popupcolor.background_color =  for_background
        


class ContentLogout(BoxLayout):
    screen = ObjectProperty()

    def __init__(self, screen, **kwargs):
        super(ContentLogout, self).__init__(**kwargs)
        self.screen = screen