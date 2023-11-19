from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.snackbar import Snackbar
from kivymd.uix.snackbar.snackbar import MDSnackbarActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.toast import toast

from components.connection import AccessDB
from kaki.app import App
import datetime
import os
from kivy.utils import platform
from plyer import filechooser


if platform == "android":
    from jnius import cast
    from jnius import autoclass
    from android import mActivity, api_version



class ImageAdd(MDScreen):

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



    def on_pre_enter(self):
        self.files = {}
        self.paths = [None]*3
        self.texto_alert = ""
        self.method = "POST"
        self.selection = ListProperty([])
        self.button = 0

        Window.bind(on_keyboard=self.voltar)
        # self._show_validation_dialog()

        Clock.schedule_once(self.verify_images, 1)






    def on_pre_leave(self):
        self.ids.image1Id.text = ""
        self.ids.image2Id.text = ""
        self.ids.image3Id.text = ""

        Window.unbind(on_keyboard=self.voltar)




    def verify_images(self, *args):
        annotation = AccessDB(name_url="annotation/image", tag="ANNOTATIONS IMAGES")
        annotation = annotation.get(self.manager.current_view_annotation)

        if type(annotation) is dict:
            self.ids.image1Id.text += annotation['image1'].split('/media/images/annotations/')[1]
            self.ids.image2Id.text += annotation['image2'].split('/media/images/annotations/')[1]
            self.ids.image3Id.text += annotation['image3'].split('/media/images/annotations/')[1]
            self.method = "PATCH"



    # form more simple of manager file
    def file_manager_open(self, button):
        if platform == 'android':
            import android
            from android.storage import primary_external_storage_path
            from android.permissions import request_permissions, Permission

            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            request_permissions([Permission.MANAGE_DOCUMENTS])

        self.button = button

        filechooser.open_file(
            title="Carica il file tempi in formato .png .jpg .jpeg",
            filters=[("Comma-separated Values", "*.png", "*.jpg", "*.jpeg")],
            on_selection=self.handle_selection
        )






    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection
        toast(selection[0], background=[0, 0, 0, 1])

        if selection != None:
            self.paths[self.button] = selection[0]
            print("VAR PATHS: "+str(self.paths))
            toast(selection[0], background=[0, 0, 0, 1])


    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        App.get_running_app().root.ids.result.text = str(self.selection)


    def send_files(self):
        data = {
            "annotation": self.manager.current_view_annotation
        }

        if self.paths[0] != None and self.paths[1] != None and self.paths[2] != None:
            self.files = {
                'image1': open(self.paths[0], 'rb'),
                'image2': open(self.paths[1], 'rb'),
                'image3': open(self.paths[2], 'rb')
            }


            # caso o user já tenha enviado
            if self.method == "PATCH":
                annotation = AccessDB(name_url="annotation/image", tag="ANNOTATIONS IMAGES")
                annotation = annotation.patch(id_object=self.manager.current_view_annotation, data=data, files=self.files)


                if type(annotation) is dict:
                    self.manager.current = "diary_list_name"
                else:
                    self.texto_alert = "Erro Ao Enviar Images"
                    Clock.schedule_once(self.alert_error_connection, 1)


            else:
                annotation = AccessDB(name_url="annotation/image/", tag="ANNOTATIONS IMAGES")
                annotation = annotation.post(data=data, files=self.files)


                if type(annotation) is bool:
                    self.manager.current = "diary_list_name"
                else:
                    self.texto_alert = "Erro Ao Enviar Images"
                    Clock.schedule_once(self.alert_error_connection, 1)

        else:
            self.texto_alert = "Missing Files, Please Upload All Files"
            Clock.schedule_once(self.alert_error_connection, 1)



    def voltar(self, key, keyboard, window, scancode=None, codepoint=None, modifier=None, *args):
        print("key: "+str(key))
        print("keyboard: "+str(keyboard))
        if keyboard in (1001, 27):
            self.manager.current = "diary_name"
            return True

        return False
