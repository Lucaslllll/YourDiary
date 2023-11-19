import os
from kivy.core.window import Window
from kivy.utils import platform

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup





if platform == "android":
    from jnius import cast
    from jnius import autoclass, PythonJavaClass, java_method
    from android import mActivity, api_version







class AudioInterface(MDBoxLayout):
    audio = ObjectProperty()

    has_recording = False

    def start_recording(self):
        state = self.audio.state
        if state == "ready":
            self.audio.start()
        if state == "recording":
            self.audio.stop()

        self.update_labels()

        raise NotImplementedError()

    def start_playing(self):
        state = self.audio.state
        if state == "playing":
            self.audio.stop()
        else:
            self.audio.play()
        self.update_labels()    

        raise NotImplementedError()


    def update_labels(self):
        record_button = self.ids['record_button']
        play_button = self.ids['play_button']
        state_label = self.ids['state']      

        state = self.audio.state
        play_button.disabled = not self.has_recording

        state_label.text = "AudioPlayer State: " + state

        if state == "ready":
            state_label.text = "START RECORD"

        if state == "recording":
            record_button.text = "STOP RECORD"
            play_button.disabled = True


        if state == "playing":
            play_button.text = "STOP AUDIO"
            record_button.disabled = True
        else:
            play_button.text = "PLAY AUDIO"
            record_button.disabled = False

        raise NotImplementedError()





class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)



class Test(MDScreen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    # def __init__(self, **kwargs):
    #     super(Test, self).__init__(**kwargs)

    def on_pre_enter(self):
        # self.check_and_request_manage_external_storage()
        # self.request_manage_external_storage()
        pass


    def open_file_chooser(self):
        if platform == "android":
          from android.permissions import request_permissions, Permission
          request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
          request_permissions([Permission.MANAGE_DOCUMENTS])

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.setType("*/*")  # Todos os tipos de arquivos
        chooser = Intent.createChooser(intent, "Selecione um arquivo")
        PythonActivity.mActivity.startActivityForResult(chooser, 1234)

    # Chamado quando a atividade do seletor de arquivos é encerrada
    def on_activity_result(self, requestCode, resultCode, intent):
        if requestCode == 1234:
            if resultCode == -1:  # RESULT_OK
                file_uri = intent.getData()
                file_path = self.get_file_path_from_uri(file_uri)
                if file_path:
                    print("Caminho do arquivo selecionado:", file_path)
                else:
                    print("Não foi possível obter o caminho do arquivo.")

    def get_file_path_from_uri(self, uri):
        content_resolver = self.get_context().getContentResolver()
        cursor = content_resolver.query(uri, [android.provider.MediaStore.MediaColumns.DATA], None, None, None)
        if cursor is not None:
            cursor.moveToFirst()
            file_path = cursor.getString(cursor.getColumnIndex(android.provider.MediaStore.MediaColumns.DATA))
            cursor.close()
            return file_path

    def get_context(self):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        return PythonActivity.mActivity




    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        PATH = "."
        if platform == "android":
          from android.permissions import request_permissions, Permission
          request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
          request_permissions([Permission.MANAGE_DOCUMENTS])
          app_folder = os.path.dirname(os.path.abspath(__file__))
          PATH = "/storage/emulated/0" #app_folder
        content.ids.filechooser.path = PATH

        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        PATH = "."
        if platform == "android":
          from android.permissions import request_permissions, Permission
          request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
          request_permissions([Permission.MANAGE_DOCUMENTS])
          app_folder = os.path.dirname(os.path.abspath(__file__))
          PATH = "/storage/emulated/0" #app_folder
        content.ids.filechooser.path = PATH
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))

        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        toast(path)
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()
