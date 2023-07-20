from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.metrics import dp

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

        #try to do this, it will allow you to have access to all directories and files in the storage.
        # if platform == "android":
        #     PythonActivity = autoclass("org.kivy.android.PythonActivity")
        #     Environment = autoclass("android.os.Environment")
        #     Intent = autoclass("android.content.Intent")
        #     Settings = autoclass("android.provider.Settings")
        #     Uri = autoclass("android.net.Uri")
        #     if api_version > 29:
        #         # If you have access to the external storage, do whatever you need
        #         if Environment.isExternalStorageManager():
        #             # If you don't have access, launch a new activity to show the user the system's dialog
        #             # to allow access to the external storage
        #             pass
        #         else:
        #             try:
        #                 activity = mActivity.getApplicationContext()
        #                 uri = Uri.parse("package:" + activity.getPackageName())
        #                 intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri)
        #                 currentActivity = cast(
        #                 "android.app.Activity", PythonActivity.mActivity
        #                 )
        #                 currentActivity.startActivityForResult(intent, 101)
        #             except:
        #                 intent = Intent()
        #                 intent.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
        #                 currentActivity = cast(
        #                 "android.app.Activity", PythonActivity.mActivity
        #                 )
        #                 currentActivity.startActivityForResult(intent, 101)

        path = filechooser.open_file(
            title="Carica il file tempi in formato .png .jpg .jpeg",
            filters=[("Comma-separated Values", "*.png", "*.jpg", "*.jpeg")]
        )
        print("AAAAAAAA")
        print("AAAAAAAA")
        print("AAAAAAAA")
        print("AAAAAAAA")
        print("AAAAAAAA")
        print("AAAAAAAA")
        print("VAR PATH: "+str(path))
        if path != None:
            self.paths[button] = path[0]
            print("VAR PATHS: "+str(self.paths))
            toast(path[0], background=[0, 0, 0, 1])

        print("AAAAAAAA")
        print("AAAAAAAA")
        print("AAAAAAAA")
        print("AAAAAAAA")
        print("AAAAAAAA")
        print("AAAAAAAA")


    def _show_validation_dialog(self):
        if platform == "android":
            Environment = autoclass("android.os.Environment")
            if not Environment.isExternalStorageManager():
                self.show_permission_popup = MDDialog(
                    title="Alert",
                    text="Permission to access your device's internal storage and files..",
                    size_hint=(0.6, 0.5),
                    buttons=[
                        MDFlatButton(
                            text="Allow", on_press=self.permissions_external_storage
                        ),
                        MDFlatButton(
                            text="Decline",
                            on_release=self._close_validation_dialog,
                        ),
                    ],
                )
                self.show_permission_popup.open()

    def _close_validation_dialog(self, widget):
        """Close input fields validation dialog"""
        self.show_permission_popup.dismiss()




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
        if key in (1001, 27):
            self.manager.current = "diary_name"
            return True

        return False
