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
        self.title_example = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.Aenean commodo ligula eget dolor. Aenean massa. Cum sociisnatoque penatibus et magnis dis p"\
                            
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
            date = annotation['date'].split("T")[0]

            self.ids.title_annotation.text = annotation['name']
            self.ids.image_annotation.source = annotation['thumb']
            self.ids.details_annotation.text = annotation['text']
            self.ids.toolbarNoticia.title = date
            self.ids.author_annotation.text = "Author: "+str(annotation['author'])
            self.ids.edit_annotation.text = "Edited " if annotation['edit'] else "Not Edited"
            self.ids.public_annotation.text = "Public " if annotation['public'] else "Personal"

            
            for category in annotation['category']:
                category_ob = AccessDB(name_url="categories", tag="CATEGORIES")
                category_ob = category_ob.get(id_object=category)
                self.ids.categories_annotation.add_widget(MDChip(id=str(category_ob['id']), text=category_ob['name']))


    def on_pre_leave(self):
        self.ids.categories_annotation.remove_widget(id="1")
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)


    def DropApp(self, instance_action_top_appbar_button):
        self.menu.caller = instance_action_top_appbar_button
        self.menu.open()
    
    def menu_callback(self, text_item):
        self.menu.dismiss()
        self.manager.current = text_item



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