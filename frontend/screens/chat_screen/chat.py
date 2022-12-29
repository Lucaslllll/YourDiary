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
        self.msg_other = 0
        self.msgs = [
            """Os caras estão desesperados hein. Vendo que pessoas inteligentes fora do sistema estão cada vez mais ganhando espaço perante a "opinião publica", os caras simplesmente estão queimando seus próprios "ídolos" para desmerecer a inteligência dos "outsiders". So rindo mesmo""",
            """Os caras já fazem o melhor que podem pra cercar o establishment científico e evitam ao máximo entregar o Nobel pra sujeitos desalinhados das narrativas oficiais. Dai quando um deles se desvia eles precisam empregar narrativas midiáticas pra destruir a reputação dos caras.""",
            """O que ocorre com frequência é qdo algum estudioso passa a incomodar o sistema, toma um cala boca, e nem sabe o porquê, pois não se liga nas"""        


        ]

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)
        self.update_msg_event = Clock.schedule_interval(self.update_msgs, 3)
        self.update_msg_event()

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)
        Clock.unschedule(self.update_msg_event)


    def update_msgs(self, *args):
        self.ids.box_chat.clear_widgets()
        
        messages = AccessDB(name_url="accounts/messages/", tag="MESSAGE")
        data = {
            "sender": self.manager.user_id,
            "receiver": self.manager.user_id_chat

        }
        messages = messages.post(data=data)
        
        if type(messages) is dict:
            for msg in messages["results"]:
                if msg['sender'] == self.manager.user_id:
                    self.ids.box_chat.add_widget(MessageLayout(texto=msg["text"]))
                elif msg['sender'] == self.manager.user_id_chat:
                    self.ids.box_chat.add_widget(MessageOtherLayout(texto=msg["text"]))
                else:
                    self.ids.box_chat.add_widget(MessageLayout(texto="Erro ao Sincronizar Mensagens"))


    def send_message(self):
        texto = self.ids.chat_keyboard.text
        if texto != "":
            Clock.unschedule(self.update_msg_event)


            self.ids.box_chat.add_widget(MessageLayout(texto=texto))
            self.ids.chat_keyboard.text = ""
            self.messages.append(texto)

            messages = AccessDB(name_url="accounts/messages/create/", tag="MESSAGE")
            messages = messages.post(data={"text":texto, "sender": self.manager.user_id, "receiver": self.manager.user_id_chat})


            self.update_msg_event()
            # print(self.messages)
            # self.saveData()
        
            # Clock.schedule_once(self.other_fake_user, 1)


    # function to test chat
    def other_fake_user(self, *args):
        if self.msg_other == 0:
            self.ids.box_chat.add_widget(MessageOtherLayout(texto=self.msgs[0]))
        elif self.msg_other == 2:
            self.ids.box_chat.add_widget(MessageOtherLayout(texto=self.msgs[1]))
        elif self.msg_other == 5:
            self.ids.box_chat.add_widget(MessageOtherLayout(texto=self.msgs[2]))
        print(self.msg_other)
        self.msg_other += 1
        

    def DropApp(self, instance_action_top_appbar_button):
        self.menu.caller = instance_action_top_appbar_button
        self.menu.open()
    
    def menu_callback(self, text_item):
        self.menu.dismiss()
        self.manager.current = text_item


    def voltar_android(self, *args, **kwargs):
        self.manager.current = "annotation_name"
        return True

    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            self.manager.current = "annotation_name"
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