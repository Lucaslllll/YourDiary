from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.storage.jsonstore import JsonStore

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

from kaki.app import App


from components.connection import AccessDB



class Login(MDScreen):
    path = ""
    dialog = None
    texto_alert = ""

    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)

    def on_pre_leave(self):
        Window.unbind(on_request_close=self.confirmacao)        

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


    def do_login(self, *args):
        username = self.ids.id_text_username.text
        senha = self.ids.id_text_password.text

        data = {
            "username": username,
            "password": senha,
        }

        user = AccessDB(name_url="accounts/login/", tag="ANNOTATIONS")
        resposta = user.post(data=data)
        
        if type(resposta) is dict:
            self.ids.load_spinner.active = True

            self.path = App.get_running_app().user_data_dir+"/"
            store = JsonStore(self.path+'data.json')
            store.put('user', id=resposta['id'])   
            self.manager.user_id = resposta['id'] 
            
            self.ids.id_text_username.text = ""
            self.ids.id_text_password.text = ""
            self.pass_of_login()
        else:
            # melhor usar atributo da funcao do que dessa forma abaixo
            # self.alert_error_connection(texto="Usuario ou Senha Errados!")
            self.texto_alert = resposta
            Clock.schedule_once(self.alert_error_connection, 4)
            # self.alert_error_connection()



    def pass_of_login(self, *args):
        self.load_if = True
        # self.path = App.get_running_app().user_data_dir+"/"
        

        store = JsonStore(self.path+'data.json')
        store.put('login_auth', access=True)
        
        # obs: mudar para outra tela
        self.manager.current = "diary_name"
        
    # segunda forma de passar para outra tela
    # def pass_to_register(self, *args):
    #     self.manager.current = "register_name"



    def timeout_spinner(self, *args):
        self.ids.load_spinner.active = False
      
    def on_press_spinner(self, *args):
        self.ids.load_spinner.active = True
        self.ids.load_spinner.determinate = False
        self.ids.load_spinner.determinate_time = 2
        # depois de 3 segundos executará timeout_spinner
        # desligando o spinner
        Clock.schedule_once(self.timeout_spinner, 3)


    def confirmacao(self, *args, **kwargs):
        # self.add_widget(self.dialog)

    
        self.dialog = MDDialog(
            text="Deseja realmente sair?",
            md_bg_color=(1,1,1,1),
            buttons=[
                MDFlatButton(
                    text="Não",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=self.closeDialog
                ),

                MDFlatButton(
                    text="Sair",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=App.get_running_app().stop
                ),
            ],
        )
    
        self.dialog.open()

        # tem que retorna um True para on_request_close
        # se não não abre o dialog
        return True

    def closeDialog(self, inst):
        self.dialog.dismiss()