from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import Snackbar

from kivymd.toast import toast
from kivymd.utils import asynckivy
from kivymd.icon_definitions import md_icons

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



class Diary(MDScreen):
    id_category_select = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        self.files = {}
        self.image_thumb_none = "/home/Lucas/Documentos/YourDiary/frontend/assets/imagens/yourdiary-logo.png"
        # print(App.get_running_app().get_root().root)
        self.count_global = "0"
        self.count = "0"
        self.texto_alert = ""
        
        

    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)
        Clock.schedule_once(self.on_start, 1)
        self.var_previous_page = 0 
        self.var_previous_page_global = 0
        self.var_atual_page = 1
        self.var_atual_page_global = 1
        self.var_next_page = 2
        self.var_next_page_global = 2

        self.manager.background_annotation = "assets/imagens/yourdiary-logo.png"

    def on_pre_leave(self):
        Window.unbind(on_request_close=self.confirmacao)
        self.ids.box.clear_widgets()
        self.ids.box_global.clear_widgets()
        self.ids.scroll_id.clear_widgets()


    def go_profile(self):
        self.manager.current_view_user = self.manager.user_id
        self.manager.current = "profile_name"        

    def do_logout(self):
        self.path = App.get_running_app().user_data_dir+"/"
        store = JsonStore(self.path+'data.json')

        if store.exists('login_auth'):
            store.put('login_auth', access=False)

        if store.exists('user'):
            store.put('user', id=None)


        self.manager.current = "login_name"



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
        self.global_area()


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
                    await asynckivy.sleep(1)
                    self.ids.box_global.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"], 
                                image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none, 
                                text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )
                
                       

                

        asynckivy.start(set_list_global())




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
                    await asynckivy.sleep(1)
                    self.ids.box.add_widget(
                        MDCardDiary(diary_screen=self, date_annotation=i_annotations['date'], id_annotation=i_annotations["id"], 
                                image_thumb=i_annotations["thumb"] if i_annotations["thumb"] != None else self.image_thumb_none, 
                                text=i_annotations["preview"] if i_annotations["preview"] != None else "Sem Prévia")
                    )
                
                       

                

        asynckivy.start(set_list())
        


    def refresh_callback_global(self, *args):
        

        def refresh_callback_global(interval):
            self.ids.box_global.clear_widgets()
            self.var_previous_page_global = 0
            self.var_atual_page_global = 1
            self.var_next_page_global = 2
            

            # form of documentation is bug layout where x = 0 in if
            # self.x, self.y = 0, 15
            
            self.set_list_global()
            self.ids.refresh_layout_global.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback_global, 1)


    def refresh_callback(self, *args):
        

        def refresh_callback(interval):
            self.ids.box.clear_widgets()
            self.var_previous_page = 0
            self.var_atual_page = 1
            self.var_next_page = 2
            

            # form of documentation is bug layout where x = 0 in if
            # self.x, self.y = 0, 15
            
            self.set_list()
            self.ids.refresh_layout.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)



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
            # path = os.path.join(ext_path,'Downloads')

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
        

    # fim part of form annotation

    # options of configurations

    def see_help(self):
        strin = "\n  O intuito é criar uma rede social para desabafar ou colocar as situações do dia a dia"\
                "\n  Na forma de um diário digital, onde pode vir a servir como terapia para angustias e coisas que não podemos falar para qualquer um"\

        self.dialog = MDDialog(
            title="Sobre",
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

    def see_donate(self):
        strin = "\n  Quem puder ajudar com qualquer valor para melhoria da infraestrutura, funcionalidades ou até para pagar um café :) doe"\
                "\n\n Paypal: "\
                "\n Pix: "\
                "\n\n Aplicativo em fase beta. Mais atualizações em breve... "

        self.dialog = MDDialog(
            title="Ajude o App",
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
    def confirmacao(self, *args, **kwargs):
        # self.add_widget(self.dialog)

    
        self.dialog = MDDialog(
            text="Deseja realmente sair?",
            md_bg_color=(1,1,1,1),
            buttons=[
                MDFlatButton(
                    text="Não",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=self.closeDialog
                ),

                MDFlatButton(
                    text="Sair",
                    theme_text_color="Custom",
                    text_color=(0,0,0,1),
                    on_release=App.get_running_app().stop
                ),
            ],
        )
    
        self.dialog.open()

        # tem que retorna um True para on_request_close
        # se não não abre o dialog
        return True


        

    def closeDialog(self, inst):
        self.dialog.dismiss()



class MDCardDiary(MDBoxLayout):
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



class SelectPageGlobal(MDBoxLayout):
    screen = ObjectProperty()

class SelectPage(MDBoxLayout):
    screen = ObjectProperty()



class CheckListCategory(MDBoxLayout):
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


