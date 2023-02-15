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

from kaki.app import App
from datetime import datetime
from components.connection import AccessDB



class Annotation(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_of_members_chips = []
        self.user_to_chat = None
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
        self.title_example = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"                            
        self.text_example = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)

        id_annotation = self.manager.current_view_annotation
        annotation = AccessDB(name_url="annotations", tag="ANNOTATIONS")
        annotation = annotation.get(id_object=id_annotation)
        

        

        if type(annotation) is dict:
            date = annotation['date'].split("T")[0].replace("-", "/")
            author_ob = AccessDB(name_url="accounts/users", tag="USERS")
            author_ob = author_ob.get(id_object=annotation['author'])

            self.user_to_chat = annotation['author']


            self.ids.title_annotation.text = annotation['name']
            self.ids.image_annotation.source = annotation['thumb']
            self.ids.details_annotation.text = annotation['text']
            self.ids.toolbarNoticia.title = date
            self.ids.author_annotation.text = "@"+author_ob['username']
            self.ids.edit_annotation.text = "Editado " if annotation['edit'] else "Não Editado"
            self.ids.public_annotation.text = "Público " if annotation['public'] else "Pessoal"

            
            for category in annotation['category']:
                category_ob = AccessDB(name_url="categories", tag="CATEGORIES")
                category_ob = category_ob.get(id_object=category)

                atual_chip = MDChip(id=str(category_ob['id']), text=category_ob['name'])
                self.ids.categories_annotation.add_widget(atual_chip)
                self.list_of_members_chips.append(atual_chip)

        Clock.schedule_once(self.check_favorite, 1.8)
        Clock.schedule_once(self.check_like, 2.5)



    def on_pre_leave(self):
        for chip in self.list_of_members_chips:
            self.ids.categories_annotation.remove_widget(chip)
        
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)


    def DropApp(self, instance_action_top_appbar_button):
        self.menu.caller = instance_action_top_appbar_button
        self.menu.open()
    
    def menu_callback(self, text_item):
        self.menu.dismiss()
        self.manager.current = text_item

    # ações

    def do_like(self):
        self.check_like()
        if type(self.like_check_ob) is dict:          
            
            like_ob = AccessDB(name_url="likes", tag="LIKES")
            like_ob = like_ob.delete(id_object=self.like_check_ob["results"]["id"])
            if type(like_ob) is dict:
                self.ids.id_like.icon_color = (0, 0, 0, 1)
       

        else:
            data = {
                "user": self.manager.user_id,
                "annotation": self.manager.current_view_annotation
            }
            like_ob = AccessDB(name_url="likes/", tag="LIKES")
            like_ob = like_ob.post(data=data)
            if type(like_ob) is bool: # aqui tem que dar 201 status
                self.ids.id_like.icon_color = (1, 1, 0, 1)
            
        
    def do_favorite(self):
        self.check_favorite()
        if type(self.favorite_check_ob) is dict:          
            
            favorite_ob = AccessDB(name_url="favorites", tag="FAVORITES")
            favorite_ob = favorite_ob.delete(id_object=self.favorite_check_ob["results"]["id"])
            if type(favorite_ob) is dict:
                self.ids.id_favorite.icon_color = (0, 0, 0, 1)
       

        else:
            data = {
                "user": self.manager.user_id,
                "annotation": self.manager.current_view_annotation
            }
            favorite_ob = AccessDB(name_url="favorites/", tag="FAVORITES")
            favorite_ob = favorite_ob.post(data=data)
            if type(favorite_ob) is bool: # aqui tem que dar 201 status
                self.ids.id_favorite.icon_color = (1, 1, 0, 1)


    def check_like(self, *args):
        data = {
            "id": "",
            "user": self.manager.user_id,
            "annotation": self.manager.current_view_annotation
        }
        self.like_check_ob =  AccessDB(name_url="annotations/likes/check/", tag="LIKES_CHECK")
        self.like_check_ob = self.like_check_ob.post(data=data)
        if type(self.like_check_ob) is dict:
            self.ids.id_like.icon_color = (1, 1, 0, 1) 
        else:
            self.ids.id_like.icon_color = (0, 0, 0, 1)


    def check_favorite(self, *args):
        data = {
            "id": "",
            "user": self.manager.user_id,
            "annotation": self.manager.current_view_annotation
        }
        self.favorite_check_ob =  AccessDB(name_url="annotations/favorites/check/", tag="FAVORITES_CHECK")
        self.favorite_check_ob = self.favorite_check_ob.post(data=data)
        if type(self.favorite_check_ob) is dict:
            self.ids.id_favorite.icon_color = (1, 1, 0, 1) 
        else:
            self.ids.id_favorite.icon_color = (0, 0, 0, 1)

    def go_profile(self):
        self.manager.current_view_user = self.user_to_chat
        self.manager.current = "profile_name"


    # fim ações

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
        