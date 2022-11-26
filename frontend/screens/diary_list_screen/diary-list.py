from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty

from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.swiper.swiper import MDSwiperItem
from kivymd.uix.card import MDCardSwipe

from components.connection import AccessDB
from kaki.app import App


class DiaryList(MDScreen):
    instance_to_delete = None
    dialog = None
    dialog_2 = None

    # criar no construtor é melhor para pegar o id dos widgets quando quero obter por outra classe
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.on_start, 1)

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Window.bind(on_request_close=self.voltar_android)
        
    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        Window.unbind(on_request_close=self.voltar_android)

    def on_start(self, *args):
        annotations = AccessDB(name_url="annotations", tag="ANNOTATIONS")
        annotations = annotations.get()
        
        if type(annotations) is list:
            for i_annotations in annotations:
                self.ids.idlist.add_widget(
                    SwipeToDeleteItem(note_id=i_annotations['id'], text=i_annotations['name'], url_image=i_annotations['thumb'])
                )


    # types of delete
    def on_swipe_complete(self, instance):
        self.instance_to_delete = instance

        self.dialog = MDDialog(
            text="Deseja realmente apagar essa notícia?",
            md_bg_color=(1,1,1,1),
            buttons=[
                MDFlatButton(
                    text="Não",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=self.closeDialog
                ),

                MDFlatButton(
                    text="Sim",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=self.sure_of_delete
                ),
            ],
        )
    
        self.dialog.open()

        return True





    # choices
    def closeDialog(self, inst):
        self.dialog.dismiss()

    def sure_of_delete(self, instance):
        annotations = AccessDB(name_url="annotations", tag="ANNOTATIONS")
        annotations.delete(id_noticia=self.instance_to_delete.note_id)
        
        self.ids.idlist.remove_widget(self.instance_to_delete)
        self.dialog.dismiss()
    

    # fim choices

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



class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    note_id = NumericProperty()
    url_image = StringProperty()
    managerer = DiaryList()
