from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

from kivymd.utils import asynckivy
from kivymd.icon_definitions import md_icons

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty

from kaki.app import App
import os


class Diary(MDScreen):
    id_category_select = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        self.files = {}


    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)
        

    def on_start(self, *args, **kwargs):
        # icons = list(md_icons.keys())
        
        for i in range(30):
            self.ids.scroll_id.add_widget(
                CheckListCategory(text=str(i), id_category=i)
                
                # ListItemWithCheckbox(text=f"Item {i}", icon=icons[i])
            )

    # to refresh pages
    def set_list(self):
        async def set_list():
            names_icons_list = list(md_icons.keys())[self.x:self.y]
            for name_icon in names_icons_list:
                await asynckivy.sleep(0)
                self.ids.box.add_widget(
                    MDCardDiary())
        asynckivy.start(set_list())

    def refresh_callback(self, *args):
        

        def refresh_callback(interval):
            self.ids.box.clear_widgets()
            
            # form of documentation is bug layout where x = 0 in if
            self.x, self.y = 0, 15
            
            self.set_list()
            self.ids.refresh_layout.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)


    # part of form annotation
    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True

    def select_path(self, path: str):
        self.exit_manager()
        self.files = {'thumb': open(path, 'rb')}
        toast(path)


    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()


    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()

        return True


class CheckListCategory(MDBoxLayout):
    text = StringProperty()
    id_category = NumericProperty()

    def __init__(self, text, id_category, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.id_category = id_category


    def on_checkbox_active(self, checkbox, value):
        if value:
            self.access_screen(1, self.id_category)
        else:
            self.access_screen(2, self.id_category)
            

    # 1 para adicionar and 2 para remover var type_access
    def access_screen(self, type_access, value, *args, **kwargs):
        if type_access == 1:
            self.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.id_category_select.append(value)
        elif type_access == 2:
            self.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.id_category_select.pop(value)
        # debug print(self.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.id_category_select)
        # try1 print(self.parent) pega o mdlist
        # try2 App.get_running_app().root.id_category_select.append(self.id_category)
        # try3 print(self.root)
        # try4 root.id_category_select.append() 


class MDCardDiary(MDBoxLayout):
    pass