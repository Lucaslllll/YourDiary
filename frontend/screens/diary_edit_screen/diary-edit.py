from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty

from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.swiper.swiper import MDSwiperItem
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from kivymd.toast import toast

from components.connection import AccessDB
from kaki.app import App
import datetime
import os
from kivy.utils import platform

class DiaryEdit(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)
        # sempre resetar esses valores
        self.id_category_select = []
        self.files = {}
        self.on_start()
        
    def on_start(self, *args):
        categories = AccessDB(name_url="categories/", tag="CATEGORIES")
        categories = categories.get()

        
        if type(categories) is list:
            for cat in categories:
                self.ids.scroll_edit_id.add_widget(
                    CheckEditCategory(managerer=self, text=str(cat["name"]), id_category=cat["id"])
                    
                )

        annotation = AccessDB(name_url="annotations/", tag="ANNOTATIONS")
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
        Window.unbind(on_request_close=self.voltar_android)

    # part of form annotation
    def file_manager_open(self):
        if platform != 'android' :
            self.file_manager.show(os.path.expanduser("~"))
            self.manager_open = True

        else:
            import android
            from android.storage import primary_external_storage_path
            from android.permissions import request_permissions, Permission
            
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            ext_path = primary_external_storage_path()


            print(ext_path)
            self.file_manager.show(ext_path)
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
        snackbar = Snackbar(
                text=self.texto_alert,
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


    def voltar_android(self, *args, **kwargs):
        self.manager.current = "diary_list_name"
        return True

    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            self.manager.current = "diary_list_name"
            # print(self.manager.current)
            return True

        return False
        

class CheckEditCategory(MDBoxLayout):
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