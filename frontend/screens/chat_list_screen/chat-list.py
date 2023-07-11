from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import sp
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty, ObjectProperty


from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget

from kaki.app import App
from components.connection import AccessDB


class ChatList(MDScreen):
    
    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Clock.schedule_once(self.run_list, 1)


    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        self.ids.idlist.clear_widgets()

    def run_list(self, *args):
        chats = AccessDB(name_url="accounts/chat/", tag="CHAT")
        chats = chats.post(data={"id_user":self.manager.user_id})        
        
        if type(chats) is dict:
            for chat in chats['results']:
                user_ob = AccessDB(name_url="accounts/users", tag="USERS")
                user_ob = user_ob.get(id_object=chat['sender'])
                
                if type(user_ob) is dict:
                    if user_ob["image"] != None:
                        profile_image = user_ob["image"]
                    else:
                        profile_image = "assets/imagens/none-image-user.png"


                    self.ids.idlist.add_widget(

                        ListItemCustom(
                            ImageLeftWidget(
                                source=profile_image,
                                radius=100
                            ),
                            text=user_ob['username']+" | "+chat['text'],
                            chat=self,
                            id_user_chat=chat['sender'],
                            
                            
                        )
                    )


    # old test
    # def run_list_fake(self, *args):
    #     for i in range(0, 10):
    #         self.fake_list_msgs()

    # def fake_list_msgs(self):
    #     self.ids.idlist.add_widget(

    #         OneLineAvatarListItem(
    #             ImageLeftWidget(
    #                 source="assets/imagens/yourdiary-logo.png"
    #             ),
    #             text="Single-line item with avatar",
    #         )
    #     )


    # def back_to_diary(self, *args):
    #     self.manager.current = "diary_name"


    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            self.manager.current = "diary_name"
            # print(self.manager.current)
            return True

        return False


class ListItemCustom(OneLineAvatarListItem):
    chat = ObjectProperty()
    id_user_chat = NumericProperty()
    name_user_chat = StringProperty()

    def go_chat(self):
        self.chat.manager.user_id_chat = self.id_user_chat
        self.chat.manager.current = "chat_name"