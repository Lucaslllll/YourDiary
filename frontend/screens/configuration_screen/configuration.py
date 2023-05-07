from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelThreeLine
# from kivymd import images_path
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.pickers import MDColorPicker

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
            ContentPickerColor(screen=self)
        )

        self.ids.content.add_widget(
            ContentLogout(screen=self)
        )




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

    def __init__(self, screen, **kwargs):
        super(ContentPickerColor, self).__init__(**kwargs)
        self.screen = screen


class ContentLogout(BoxLayout):
    screen = ObjectProperty()

    def __init__(self, screen, **kwargs):
        super(ContentLogout, self).__init__(**kwargs)
        self.screen = screen