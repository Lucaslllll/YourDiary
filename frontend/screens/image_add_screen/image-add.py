from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty


from kivymd.uix.snackbar import Snackbar
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


class ImageAdd(MDScreen):

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



    def on_pre_enter(self):
        self.files = {}
        self.paths = [None]*3
        self.texto_alert = ""
        self.method = "POST"

        Window.bind(on_request_close=self.voltar_android)
        Window.bind(on_keyboard=self.voltar)
        

        Clock.schedule_once(self.verify_images, 1)


    def on_pre_leave(self):
        self.ids.image1Id.text = ""
        self.ids.image2Id.text = ""
        self.ids.image3Id.text = ""        

        Window.unbind(on_request_close=self.voltar_android)
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


        path = filechooser.open_file(
            title="Carica il file tempi in formato .png .jpg .jpeg",
            filters=[("Comma-separated Values", "*.png", "*.jpg", "*.jpeg")]
        )
        if path != None:
            self.paths[button] = path[0]
            toast(path[0], background=[0, 0, 0, 1])
        



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