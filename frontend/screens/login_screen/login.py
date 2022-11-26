from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty

from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kaki.app import App





class AlertErrorSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")



class Login(MDScreen):
    path = ""
    dialog = None
    texto_alert = ""

    def alert_error_connection(self, *args):
        snackbar = AlertErrorSnackbar(
                text=self.texto_alert,
                icon="information",
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


        user = Usuario()
        resposta = user.do_login(username, senha)

        if type(resposta) is dict:
            self.ids.load_spinner.active = True

            self.path = App.get_running_app().user_data_dir+"/"
            store = JsonStore(self.path+'data.json')
            store.put('user', id=resposta['dados']['id'])    
            
            self.pass_of_login()
        else:
            # melhor usar atributo da funcao do que dessa forma abaixo
            # self.alert_error_connection(texto="Usuario ou Senha Errados!")
            self.texto_alert = resposta
            Clock.schedule_once(self.alert_error_connection, 4)
            # self.alert_error_connection()



    def pass_of_login(self, *args):
        self.load_if = True
        self.path = App.get_running_app().user_data_dir+"/"
        

        store = JsonStore(self.path+'data.json')
        store.put('login_auth', access=True)
        
        # obs: mudar para outra tela
        App.get_running_app().root.current = "login_name"
        
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

