from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons

from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard

from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kaki.app import App

from kivy.clock import Clock

class Diary(MDScreen):
    id_category_select = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    def on_pre_enter(self):
        Clock.schedule_once(self.on_start, 1)
        # self.on_start(1)

    def on_start(self, *args, **kwargs):
        # icons = list(md_icons.keys())
        
        for i in range(30):
            self.ids.scroll_id.add_widget(
                CheckListCategory(text=str(i), id_category=i)
                
                # ListItemWithCheckbox(text=f"Item {i}", icon=icons[i])
            )
        pass


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


class MDCardDiary(MDCard):
    pass