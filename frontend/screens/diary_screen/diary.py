from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.snackbar.snackbar import MDSnackbarActionButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from kivymd.toast import toast
from kivymd.utils import asynckivy

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.storage.jsonstore import JsonStore


from kaki.app import App
from kivymd.app import MDApp
import os
from components.connection import Authenticat, AccessDB
import datetime
from kivy.utils import platform
from plyer import filechooser



class Diary(MDScreen):
    id_category_select = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.files = {}
        self.image_thumb_none = "/home/Lucas/Documentos/YourDiary/frontend/assets/imagens/yourdiary-logo.png"
        # print(App.get_running_app().get_root().root)
        self.count_global = "0"
        self.count = "0"
        self.texto_alert = ""




    def on_pre_enter(self):
        Window.bind(on_keyboard=self.confirmacao)
        Clock.schedule_once(self.on_start, 1)
        self.var_previous_page = 0
        self.var_previous_page_global = 0
        self.var_atual_page = 1
        self.var_atual_page_global = 1
        self.var_next_page = 2
        self.var_next_page_global = 2

        # color toolbar and navrail
        self.ids.top_diary.md_bg_color = self.manager.color_main
        self.ids.id_nav_rail.selected_color_background = self.manager.color_main

        self.manager.background_annotation = "assets/imagens/yourdiary-logo.png"

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.confirmacao)
        self.ids.box.clear_widgets()
        self.ids.box_global.clear_widgets()
        self.ids.scroll_id.clear_widgets()


    def go_profile(self):
        self.manager.current_view_user = self.manager.user_id
        self.manager.current = "profile_name"




    def on_start(self, *args, **kwargs):

        # list of categories of form
        categories = AccessDB(name_url="categories", tag="CATEGORIES")
        categories = categories.get()


        if type(categories) is list:
            for cat in categories:
                self.ids.scroll_id.add_widget(
                    CheckListCategory(managerer=self, text=str(cat["name"]), id_category=cat["id"])

                )
        # fim
        self.personal_area()
        # self.ids.box_global.clear_widgets()
        # self.global_area()


    def star_area(self):
        annotations = AccessDB(name_url="annotations/favorites", tag="ANNOTATIONS_FAVORITES")
        annotations = annotations.get(id_object=self.manager.user_id)
        self.ids.box_global.clear_widgets()

        async def star_area():
            self.count_global = str(self.var_atual_page_global)
            self.ids.box_global.add_widget(
                    SelectPageStar(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(1)
                    self.ids.box_global.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                    image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                    text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )


        self.var_previous_page_global = 0
        self.var_atual_page_global = 1
        self.var_next_page_global = 2

        asynckivy.start(star_area())

    def next_page_star(self, voltar=False):
        self.ids.box_global.clear_widgets()


        if voltar == False:
            # para frente
            annotations = AccessDB(name_url="annotations/favorites", tag="ANNOTATIONS_FAVORITES")
            annotations = annotations.filter_by_id(id_object=self.manager.user_id, page=self.var_next_page_global)


            self.var_previous_page_global = self.var_atual_page_global
            self.var_atual_page_global = self.var_next_page_global
            self.var_next_page_global += 1



        elif voltar == True:
            # para trás
            annotations = AccessDB(name_url="annotations/favorites", tag="ANNOTATIONS_FAVORITES")
            annotations = annotations.filter_by_id(id_object=self.manager.user_id, page=self.var_previous_page_global)


            self.var_atual_page_global = self.var_previous_page_global
            self.var_previous_page_global = self.var_atual_page_global - 1
            self.var_next_page_global = self.var_atual_page_global + 1



        async def next_page_star():
            self.count_global = str(self.var_atual_page_global)
            self.ids.box_global.add_widget(
                        SelectPageStar(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(1)
                    self.ids.box_global.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                    image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                    text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )


        asynckivy.start(next_page_star())




    def following_area(self):
        annotations = AccessDB(name_url="accounts/followings", tag="ANNOTATIONS")
        annotations = annotations.get(id_object=self.manager.user_id)
        self.ids.box_global.clear_widgets()

        async def following_area():
            self.count_global = str(self.var_atual_page_global)
            self.ids.box_global.add_widget(
                    SelectPageFollowing(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(1)
                    self.ids.box_global.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                    image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                    text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )


        self.var_previous_page_global = 0
        self.var_atual_page_global = 1
        self.var_next_page_global = 2

        asynckivy.start(following_area())




    def next_page_following(self, voltar=False):
        self.ids.box_global.clear_widgets()



        if voltar == False:
            # para frente
            annotations = AccessDB(name_url="accounts/followings", tag="FOLLOWINGS")
            annotations = annotations.filter_by_id(id_object=self.manager.user_id, page=self.var_next_page_global)


            self.var_previous_page_global = self.var_atual_page_global
            self.var_atual_page_global = self.var_next_page_global
            self.var_next_page_global += 1



        elif voltar == True:
            # para trás
            annotations = AccessDB(name_url="accounts/followings", tag="FOLLOWINGS")
            annotations = annotations.filter_by_id(id_object=self.manager.user_id, page=self.var_previous_page_global)


            self.var_atual_page_global = self.var_previous_page_global
            self.var_previous_page_global = self.var_atual_page_global - 1
            self.var_next_page_global = self.var_atual_page_global + 1



        async def next_page_following():
            self.count_global = str(self.var_atual_page_global)
            self.ids.box_global.add_widget(
                        SelectPageFollowing(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(1)
                    self.ids.box_global.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                    image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                    text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )




        asynckivy.start(next_page_following())





    def global_area(self):
        annotations = AccessDB(name_url="annotations/public", tag="ANNOTATIONS")
        annotations = annotations.get()


        async def global_area():
            self.count_global = str(self.var_atual_page_global)
            self.ids.box_global.add_widget(
                    SelectPageGlobal(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(1)
                    self.ids.box_global.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                    image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                    text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )





        asynckivy.start(global_area())



    def next_page_global(self, voltar=False):
        self.ids.box_global.clear_widgets()



        if voltar == False:
            # para frente
            annotations = AccessDB(name_url="annotations/public", tag="ANNOTATIONS")
            annotations = annotations.get(id_object=self.manager.user_id, page=self.var_next_page_global)


            self.var_previous_page_global = self.var_atual_page_global
            self.var_atual_page_global = self.var_next_page_global
            self.var_next_page_global += 1



        elif voltar == True:
            # para trás
            annotations = AccessDB(name_url="annotations/public", tag="ANNOTATIONS")
            annotations = annotations.get(id_object=self.manager.user_id, page=self.var_previous_page_global)


            self.var_atual_page_global = self.var_previous_page_global
            self.var_previous_page_global = self.var_atual_page_global - 1
            self.var_next_page_global = self.var_atual_page_global + 1



        async def next_page_global():
            self.count_global = str(self.var_atual_page_global)
            self.ids.box_global.add_widget(
                        SelectPageGlobal(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(1)
                    self.ids.box_global.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                    image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                    text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )




        asynckivy.start(next_page_global())


    # to refresh pages
    def set_list_global(self):
        annotations = AccessDB(name_url="annotations/public", tag="ANNOTATIONS")
        annotations = annotations.get()

        async def set_list_global():
            self.count_global = str(self.var_atual_page_global)
            self.ids.box_global.add_widget(
                    SelectPageGlobal(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(0.1)
                    self.ids.box_global.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )





        asynckivy.start(set_list_global())



    def refresh_callback_global(self, *args):
        # self.ids.idNavRail.switch_tab(0)
        # self.ids.id_filter_todos.active = True
        self.ids.box_global.clear_widgets()

        def refresh_callback_global(interval):

            self.var_previous_page_global = 0
            self.var_atual_page_global = 1
            self.var_next_page_global = 2


            # form of documentation is bug layout where x = 0 in if
            # self.x, self.y = 0, 15

            self.set_list_global()
            self.ids.refresh_layout_global.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback_global, 0.5)



    def personal_area(self):
        annotations = AccessDB(name_url="annotations/by/author", tag="ANNOTATIONS")
        annotations = annotations.filter_by_id(id_object=self.manager.user_id)

        async def personal_area():
            self.count = str(self.var_atual_page)
            self.ids.box.add_widget(
                    SelectPage(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(1)
                    self.ids.box.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                    image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                    text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )





        asynckivy.start(personal_area())





    def next_page(self, voltar=False):
        self.ids.box.clear_widgets()



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



        async def next_page():
            self.count = str(self.var_atual_page)
            self.ids.box.add_widget(
                        SelectPage(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(1)
                    self.ids.box.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                    image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                    text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )




        asynckivy.start(next_page())





    def set_list(self):
        annotations = AccessDB(name_url="annotations/by/author", tag="ANNOTATIONS")
        annotations = annotations.filter_by_id(id_object=self.manager.user_id)

        async def set_list():
            self.count = str(self.var_atual_page)
            self.ids.box.add_widget(
                    SelectPage(screen=self)
            )

            if type(annotations) is dict:

                for i_annotations in annotations["results"]:
                    await asynckivy.sleep(0.1)
                    self.ids.box.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"],
                                image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none,
                                text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )





        asynckivy.start(set_list())



    def refresh_callback(self, *args):
        self.ids.box.clear_widgets()

        def refresh_callback(interval):

            self.var_previous_page = 0
            self.var_atual_page = 1
            self.var_next_page = 2


            # form of documentation is bug layout where x = 0 in if
            # self.x, self.y = 0, 15

            self.set_list()
            self.ids.refresh_layout.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 0.5)



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
            "edit": False,
            "author": self.manager.user_id,
            "category": self.id_category_select,
        }

        annotation = AccessDB(name_url="annotations/", tag="ANNOTATIONS")
        resposta = annotation.post(data=data, files=self.files)

        if resposta == True:
            self.clear_form()
            self.manager.current = "diary_list_name"
        else:
            self.texto_alert = resposta
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


    # fim part of form annotation

    # options of configurations

    def see_donate(self):
        strin = "\nAnyone who can help with any amount to improve the infrastructure, features or even to pay for a coffee :) donate"\
                "\n\n\nPaypal: lucascosta12367@gmail.com"\
                "\n\n\nApplication in beta phase. More updates coming soon... "
                # Pix: 84 99489-7318

        self.dialog = MDDialog(
            title="Help The App",
            text=strin,
            md_bg_color=(1,1,1,1),
            buttons=[
                MDFlatButton(
                    text="Sair",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=self.closeDialog
                ),
            ],
        )

        self.dialog.open()

    # sair do app
    def confirmacao(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            self.dialog = MDDialog(
            text="Do you really want to leave?",
            md_bg_color=(1,1,1,1),
            buttons=[
                    MDFlatButton(
                        text="No",
                        theme_text_color="Custom",
                        text_color=(0,0,0,1),
                        on_release=self.closeDialog
                    ),

                    MDFlatButton(
                        text="Exit",
                        theme_text_color="Custom",
                        text_color=(0,0,0,1),
                        on_release=App.get_running_app().stop
                    ),
                ],
            )
            self.dialog.open()

            return True

        return False




    def closeDialog(self, inst):
        self.dialog.dismiss()


    def go_search(self):
        self.manager.current = "search_name"



class MDCardDiary(BoxLayout):
    id_annotation = NumericProperty()
    image_thumb = StringProperty()
    text = StringProperty()
    date_annotation = StringProperty()
    image_thumb_none = "/home/Lucas/Documentos/YourDiary/frontend/assets/imagens/yourdiary-logo.png"
    diary_screen = ObjectProperty()

    def __init__(self, diary_screen, date_annotation, id_annotation=-1, text="none", image_thumb=image_thumb_none, **kwargs):
        super(MDCardDiary, self).__init__(**kwargs)
        self.text = text
        self.id_annotation = id_annotation
        self.image_thumb = image_thumb
        self.diary_screen = diary_screen
        if date_annotation != None:
            self.date_annotation = date_annotation.split("T")[0].replace("-", "/")

        else:
            self.date_annotation = "Unknown Date"

    def read_more(self):
        self.diary_screen.manager.current_view_annotation = self.id_annotation
        self.diary_screen.manager.current = "annotation_name"



class SelectPageStar(BoxLayout):
    screen = ObjectProperty()

class SelectPageFollowing(BoxLayout):
    screen = ObjectProperty()

class SelectPageGlobal(BoxLayout):
    screen = ObjectProperty()

class SelectPage(BoxLayout):
    screen = ObjectProperty()



class CheckListCategory(BoxLayout):
    text = StringProperty()
    id_category = NumericProperty()
    managerer = ObjectProperty()

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
            #funfa too self.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.id_category_select.append(value)
        elif type_access == 2:
            self.managerer.id_category_select.remove(value)
            #funfa too self.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.id_category_select.pop(value)

        ## debug
        # print(self.managerer.id_category_select)
        # try1 print(self.parent) pega o mdlist
        # try2 App.get_running_app().root.id_category_select.append(self.id_category)
        # try3 print(self.root)
        # try4 root.id_category_select.append()
