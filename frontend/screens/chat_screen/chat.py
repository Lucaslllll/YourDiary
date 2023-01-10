from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import sp
from kivy.uix.label import Label

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip
from kivymd.uix.boxlayout import MDBoxLayout

from kaki.app import App
from datetime import datetime
from components.connection import AccessDB
from kivymd.utils import asynckivy
import requests
import json
from components.crypto import USERNAME, PASSWORD



class Chat(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        self.update_msg_event = None
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Home",
                "height": 56,
                "on_release": lambda x="Home": self.menu_callback("diary_name"),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Menu",
                "height": 56,
                "on_release": lambda x="Menu": self.menu_callback("diary_list_name"),
            }

        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        self.last_msg = ""
        self.count_msg = 0
        


    def on_pre_enter(self):
        self.sender = self.manager.user_id,
        self.receiver = self.manager.user_id_chat
        self.token_access = ""

        self.update_do_auth = Clock.schedule_interval(self.optimization_do_auth, 120)
        self.update_do_auth()
        self.optimization_do_auth()

        self.update_msg_event = Clock.schedule_interval(self.update_msgs, 5)
        self.update_msg_event() # intervalo para ficar rodando
        # self.update_msgs() # executa primeiro
        

        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)
        

    def on_pre_leave(self):
        self.ids.box_chat.clear_widgets()
        self.update_do_auth.cancel()
        self.update_msg_event.cancel()
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)
        # zerar as variáveis que checka as ultimas msgs do chat
        self.count_msg = 0 
        self.last_msg = ""


    def optimization_do_auth(self, *args):
        valores = {
            "username":USERNAME,
            "password":PASSWORD
        }
        


        try:
            requisicao = requests.post("http://143.198.165.63/token", data=valores)
        except:
            return None

        dic_content = requisicao.json()
        self.token_access = dic_content["access"]
        
        return self.token_access


    # function to test optimization of routes
    def optimization_route_chat(self):
        data = {
            "sender": self.sender,
            "receiver": self.receiver
        }

        head = {'Authorization': 'Bearer {}'.format(self.token_access)}

        requisicao = requests.post("http://143.198.165.63/accounts/messages/", data=data, headers=head)

        if requisicao.status_code == 201:
            return True
        elif requisicao.status_code == 200:
            return requisicao.json()
        elif requisicao.status_code == 401:
            return "Sem Autorização"
        elif requisicao.status_code == 400:
            return "Falta ou Dado Já Repetido Por Outros"
        else:
            return "Erro Inesperado"


    def update_msgs(self, *args):

        async def update_msgs():
            

            # await asynckivy.sleep(1)

            messages = self.optimization_route_chat()
            
            if type(messages) is dict and len(messages['results']) != 0:
                if messages['results'][-1]['date'] != self.last_msg:
                    if self.count_msg == 0:    

                        for msg in messages["results"]:
                            if msg['sender'] == self.manager.user_id:
                                self.ids.box_chat.add_widget(MessageLayout(texto=msg["text"]))
                            elif msg['sender'] == self.manager.user_id_chat:
                                self.ids.box_chat.add_widget(MessageOtherLayout(texto=msg["text"]))
                            else:
                                self.ids.box_chat.add_widget(MessageLayout(texto="Erro ao Sincronizar Mensagens"))

                        self.last_msg = messages['results'][-1]['date']
                        self.count_msg = 1
                    

                    else:
                        self.last_msg = messages['results'][-1]['date']

                        if messages['results'][-1]['sender'] == self.manager.user_id:
                                self.ids.box_chat.add_widget(MessageLayout(texto=messages['results'][-1]["text"]))
                        elif messages['results'][-1]['sender'] == self.manager.user_id_chat:
                            self.ids.box_chat.add_widget(MessageOtherLayout(texto=messages['results'][-1]["text"]))



        asynckivy.start(update_msgs())


    def send_message(self):
        texto = self.ids.chat_keyboard.text
        if texto != "":
            # Clock.unschedule(self.update_msg_event)
            self.update_msg_event.cancel()

            self.update_msgs()
            
            # self.ids.box_chat.add_widget(MessageLayout(texto=texto)) gera duplicada nessa atualização de codigo
            self.ids.chat_keyboard.text = ""
            self.messages.append(texto)

            messages = AccessDB(name_url="accounts/messages/create/", tag="MESSAGE")
            messages = messages.post(data={"text":texto, "sender": self.manager.user_id, "receiver": self.manager.user_id_chat})

            self.update_msg_event()
        


    # function to test chat
    def other_fake_user(self, *args):
        if self.msg_other == 0:
            self.ids.box_chat.add_widget(MessageOtherLayout(texto=self.msgs[0]))
        elif self.msg_other == 2:
            self.ids.box_chat.add_widget(MessageOtherLayout(texto=self.msgs[1]))
        elif self.msg_other == 5:
            self.ids.box_chat.add_widget(MessageOtherLayout(texto=self.msgs[2]))
        # print(self.msg_other)
        self.msg_other += 1
        

    def DropApp(self, instance_action_top_appbar_button):
        self.menu.caller = instance_action_top_appbar_button
        self.menu.open()
    
    def menu_callback(self, text_item):
        self.menu.dismiss()
        self.manager.current = text_item


    def voltar_android(self, *args, **kwargs):
        self.manager.current = "chat_list_name"
        return True

    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            self.manager.current = "chat_list_name"
            # print(self.manager.current)
            return True

        return False



class MessageLayout(MDBoxLayout):
    def __init__(self, texto, **kwargs):
        super().__init__(**kwargs)
        self.text = texto
        self.add_widget(Message(text=self.text))
        


class Message(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.font_size = sp(12)

    def on_size(self, *args):
        self.text_size = (self.width - sp(10), None)

    def on_texture_size(self, *args):
        self.size = self.texture_size
        self.height += sp(20)


class MessageOtherLayout(MDBoxLayout):
    def __init__(self, texto, **kwargs):
        super().__init__(**kwargs)
        self.text = texto
        self.add_widget(MessageOther(text=self.text))
        


class MessageOther(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.font_size = sp(12)

    def on_size(self, *args):
        self.text_size = (self.width - sp(10), None)

    def on_texture_size(self, *args):
        self.size = self.texture_size
        self.height += sp(20)