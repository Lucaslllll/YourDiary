from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty


from kivymd.uix.snackbar import Snackbar
from kivymd.uix.snackbar.snackbar import MDSnackbarActionButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.chip import MDChip
from kivymd.uix.list import TwoLineListItem, TwoLineAvatarIconListItem

from kaki.app import App
from components.connection import AccessDB
# from kivy.base import EventLoop
from kivy.core.window import Window




class Search(MDScreen):
    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)

    def reload_search(self):
        data = {
            "text": self.ids.idSearchText.text,
        }

        annotations = AccessDB(name_url="annotation/search/", tag="SEARCH ANNOTATIONS")
        annotations = annotations.post(data=data)


        if type(annotations) is dict:
            self.ids.annotations.clear_widgets()
            self.ids.spinner.active = True
            Clock.schedule_once(self.timeout_spinner, 4)

            for i_annotations in annotations['results']:
                self.ids.annotations.add_widget(
                    MDCardDiarySearch(diary_screen=self, id_annotation=i_annotations['id'], text=i_annotations['name'], date_annotation=i_annotations['date'])
                )

    def timeout_spinner(self, *args):
        self.ids.spinner.active = False

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        self.ids.annotations.clear_widgets()

    def voltar(self, window, key, keycode, *args):
        # esc tem o codigo 27
        if key == 27 or key == 41:
            self.manager.current = "diary_name"
            # print(self.manager.current)
            return True
        return False





class MDCardDiarySearch(BoxLayout):
    id_annotation = NumericProperty()
    text = StringProperty()
    date_annotation = StringProperty()
    diary_screen = ObjectProperty()

    def __init__(self, diary_screen, date_annotation, id_annotation=-1, text="none", *args, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.id_annotation = id_annotation
        self.diary_screen = diary_screen

        if date_annotation != None:
            self.date_annotation = date_annotation.split("T")[0].replace("-", "/")

        else:
            self.date_annotation = "Unknown Date"

    def read_more(self):
        self.diary_screen.manager.current_view_annotation = self.id_annotation
        self.diary_screen.manager.current = "annotation_name"





class ChipFilter(MDChip):
    pass
