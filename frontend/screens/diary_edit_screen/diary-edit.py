from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from kivymd.uix.snackbar import Snackbar
from kivymd.uix.snackbar.snackbar import MDSnackbarActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from kivymd.toast import toast

from components.connection import AccessDB
from kaki.app import App
import datetime
import os
from kivy.utils import platform
from plyer import filechooser


class DiaryEdit(MDScreen):

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        # sempre resetar esses valores
        self.id_category_select = []
        self.files = {}
        self.on_start()
        
    def on_start(self, *args):
        categories = AccessDB(name_url="categories", tag="CATEGORIES")
        categories = categories.get()

        
        if type(categories) is list:
            for cat in categories:
                self.ids.scroll_edit_id.add_widget(
                    CheckEditCategory(managerer=self, text=str(cat["name"]), id_category=cat["id"])
                    
                )

        annotation = AccessDB(name_url="annotations", tag="ANNOTATIONS")
        user_ob = annotation.get(id_object=self.manager.current_view_annotation)

        if type(user_ob) is dict:
            self.ids.id_note_name.text = user_ob['name']
            self.ids.id_note_preview.text = user_ob['preview']
            self.ids.id_note_text.text = user_ob['text']
            self.ids.id_note_public.active = user_ob['public']
            self.id_category_select = []

            
            

    def on_pre_leave(self):
        self.ids.scroll_edit_id.clear_widgets()
        Window.unbind(on_keyboard=self.voltar)

    # part of form annotation
    def file_manager_open(self):
        path = filechooser.open_file(
            title="Carica il file tempi in formato .png .jpg .jpeg",
            filters=[("Comma-separated Values", "*.png", "*.jpg", "*.jpeg")]
        )
        if path != None:            
            self.files = {'thumb': open(path[0], 'rb')}
            toast(path[0], background=[0, 0, 0, 1])


    def send_annotation(self, *args):
        data = {
            "name": self.ids.id_note_name.text,
            "preview": self.ids.id_note_preview.text,
            "text": self.ids.id_note_text.text,
            "date": datetime.datetime.now(),
            "public": self.ids.id_note_public.active,
            "edit": True,
            "author": self.manager.user_id,
            "category": self.id_category_select,
        }

        annotation = AccessDB(name_url="annotations", tag="ANNOTATIONS")
        resposta = annotation.put(id_object=self.manager.current_view_annotation, data=data, files=self.files)

        if type(resposta) is dict:
            self.clear_form()
            self.manager.current = "diary_list_name"
        else:
            self.texto_alert = "miss some field, try send a image"
            Clock.schedule_once(self.alert_error_connection, 3)


    def alert_error_connection(self, *args):
        Snackbar(
            MDLabel(
                text=self.texto_alert,
                theme_text_color="Custom",
                text_color="#393231",
            ),
            MDSnackbarActionButton(
                text="close",
                theme_text_color="Custom",
                text_color="#8E353C",
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            md_bg_color="#E8D8D7",
        ).open()



    def timeout_spinner(self, *args):
        self.ids.load_spinner_note.active = False
      
    def on_press_spinner(self, *args):
        self.ids.load_spinner_note.active = True
        self.ids.load_spinner_note.determinate = False
        self.ids.load_spinner_note.determinate_time = 2
        # depois de 3 segundos executará timeout_spinner
        # desligando o spinner
        Clock.schedule_once(self.timeout_spinner, 3)

    def clear_form(self):
        self.ids.id_note_name.text = ""
        self.ids.id_note_preview.text = ""
        self.ids.id_note_text.text = ""
        self.ids.id_note_public.active = False


    def voltar(self, window, key, *args):
        if key == 27:
            self.manager.current = "diary_list_name"
            return True

        return False
        

class CheckEditCategory(BoxLayout):
    text = StringProperty()
    id_category = NumericProperty()
    managerer = ObjectProperty()


    # número de atributos definidos em cima tem que ser colocados no construtor
    # ou não sobreescreva o construtor, igual SwipeToDeleteItem de diary-list
    def __init__(self, managerer, text, id_category, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.id_category = id_category
        self.managerer = managerer


    def on_checkbox_active(self, checkbox, value):
        if value:
            self.access_screen(1, self.id_category)
        else:
            self.access_screen(2, self.id_category)
            

    # 1 para adicionar and 2 para remover var type_access
    def access_screen(self, type_access, value, *args, **kwargs):
        if type_access == 1:
            self.managerer.id_category_select.append(value)
        elif type_access == 2:
            self.managerer.id_category_select.remove(value)