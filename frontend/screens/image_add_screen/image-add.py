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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.files = {}
        self.paths = []
        


    # form more simple of manager file
    def file_manager_open(self):
        path = filechooser.open_file(
            title="Carica il file tempi in formato .png .jpg .jpeg",
            filters=[("Comma-separated Values", "*.png", "*.jpg", "*.jpeg")]
        )
        if path != None:
            self.paths.append(path[0])
            toast(path[0], background=[0, 0, 0, 1])
        



    def send_files(self):
        data = {
            "annotation": self.manager.current_view_annotation
        }

        
        self.files = {
            'image1': open(self.paths[0], 'rb'), 
            'image2': open(self.paths[1], 'rb'),
            'image3': open(self.paths[2], 'rb')
        }
        
        annotation = AccessDB(name_url="annotation/image/", tag="ANNOTATIONS IMAGES")
        annotation = annotation.post(data=data, files=self.files)
