from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty


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
        

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        Clock.schedule_once(self.on_start, 1)
        self.var_previous_page = 0
        self.var_atual_page = 1
        self.var_next_page = 2

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        self.ids.idlist.clear_widgets()

    def on_start(self, *args):
        annotations = AccessDB(name_url="annotations/by/author", tag="ANNOTATIONS")
        annotations = annotations.filter_by_id(id_object=self.manager.user_id)
        

        if type(annotations) is dict:
            for i_annotations in annotations["results"]:
                self.ids.idlist.add_widget(
                    SwipeToDeleteItem(diary_list_screen=self, id_annotation=i_annotations['id'], text=i_annotations['name'], url_image=i_annotations['thumb'])
                )



    def next_page(self, page, voltar=False):
        self.ids.idlist.clear_widgets()

        annotations = AccessDB(name_url="annotations/by/author", tag="ANNOTATIONS")
        annotations = annotations.filter_by_id(id_object=self.manager.user_id, page=page)

        

        if voltar == False:
            # para frente
            annotations = AccessDB(name_url="annotations/by/author", tag="ANNOTATIONS")
            annotations = annotations.filter_by_id(id_object=self.manager.user_id, page=self.var_next_page)


            self.var_previous_page = self.var_atual_page
            self.var_atual_page = self.var_next_page
            self.var_next_page += 1


        
        elif voltar == True:
            # para trás
            annotations = AccessDB(name_url="annotations/by/author", tag="ANNOTATIONS")
            annotations = annotations.filter_by_id(id_object=self.manager.user_id, page=self.var_previous_page)
            

            self.var_atual_page = self.var_previous_page
            self.var_previous_page = self.var_atual_page - 1
            self.var_next_page = self.var_atual_page + 1


        if type(annotations) is dict:
            for i_annotations in annotations["results"]:
                self.ids.idlist.add_widget(
                    SwipeToDeleteItem(diary_list_screen=self, id_annotation=i_annotations['id'], text=i_annotations['name'], url_image=i_annotations['thumb'])
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
        annotations.delete(id_object=self.instance_to_delete.id_annotation)
        
        self.ids.idlist.remove_widget(self.instance_to_delete)
        self.dialog.dismiss()
    

    # fim choices

    def voltar(self, window, key, *args):
        if key == 27 or key == 41:
            self.manager.current = "diary_name"
            return True

        return False



class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    id_annotation = NumericProperty()
    date_annotation = StringProperty("Unknown")
    url_image = StringProperty()
    diary_list_screen = ObjectProperty()


    def edit_annotation(self):
        self.diary_list_screen.manager.current_view_annotation = self.id_annotation
        self.diary_list_screen.manager.current = "diary_edit_name"

    def add_image(self):
        self.diary_list_screen.manager.current_view_annotation = self.id_annotation
        self.diary_list_screen.manager.current = "image_add_name"



