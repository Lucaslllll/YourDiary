from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ObjectProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip
from kivymd.uix.swiper.swiper import MDSwiperItem
from kivymd.uix.fitimage.fitimage import FitImage
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from kaki.app import App
from components.connection import AccessDB
from kivy.metrics import sp, dp


class Annotation(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_of_members_chips = []
        self.list_of_members_swiper = []
        self.user_to_chat = None
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Home",
                "height": 56,
                "on_release": lambda x="Home": self.menu_callback("diary_name"),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Menu",
                "height": 56,
                "on_release": lambda x="Menu": self.menu_callback("diary_list_name"),
            }

        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,

        )
        self.title_example = "example title"
        self.text_example = "Lorem ipsum dolor"
        

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)
        
        # set color toolbar 
        self.ids.toolbarNoticia.md_bg_color = self.manager.color_main
        self.ids.toolbarNoticia.back_layer_color = self.manager.color_main

        self.start_image()
        self.start_content()
        
        Clock.schedule_once(self.check_favorite, 1.8)
        Clock.schedule_once(self.check_like, 2.3)



    def start_image(self):
        images_ob = AccessDB(name_url="annotation/image/filter", tag="CATEGORIES")
        images_ob = images_ob.get(id_object=self.manager.current_view_annotation)
        

        if type(images_ob) is dict:
            if len(images_ob['results']) == 1:
                swiper1 = CustomSwiper(image=images_ob['results'][0]['image1'])
                swiper2 = CustomSwiper(image=images_ob['results'][0]['image2'])
                swiper3 = CustomSwiper(image=images_ob['results'][0]['image3'])
                
                self.list_of_members_swiper = [swiper1, swiper2, swiper3]

                self.ids.image_annotation.add_widget(swiper1)
                self.ids.image_annotation.add_widget(swiper2)
                self.ids.image_annotation.add_widget(swiper3)


    def start_content(self):
        id_annotation = self.manager.current_view_annotation
        annotation = AccessDB(name_url="annotations", tag="ANNOTATIONS")
        annotation = annotation.get(id_object=id_annotation)

        if type(annotation) is dict:
            date = annotation['date'].split("T")[0].replace("-", "/")
            author_ob = AccessDB(name_url="accounts/users", tag="USERS")
            author_ob = author_ob.get(id_object=annotation['author'])

            self.user_to_chat = annotation['author']


            self.ids.title_annotation.text = annotation['name']
            self.ids.details_annotation.text = annotation['text']
            self.ids.toolbarNoticia.title = date 
            self.ids.author_annotation.text = "@"+author_ob['username']
            self.ids.edit_annotation.text = "Edited " if annotation['edit'] else "No Edited"
            self.ids.public_annotation.text = "Public " if annotation['public'] else "Private"

            
            for category in annotation['category']:
                category_ob = AccessDB(name_url="categories", tag="CATEGORIES")
                category_ob = category_ob.get(id_object=category)

                atual_chip = MDChip(id=str(category_ob['id']), text=category_ob['name'])
                self.ids.categories_annotation.add_widget(atual_chip)
                self.list_of_members_chips.append(atual_chip)

                

    def on_pre_leave(self):
        for chip in self.list_of_members_chips:
            self.ids.categories_annotation.remove_widget(chip)
        
        
        for i in self.list_of_members_swiper:
            self.ids.image_annotation.remove_widget(i)
        
        Window.unbind(on_keyboard=self.voltar)


    def DropApp(self, instance_action_top_appbar_button):
        self.menu.caller = instance_action_top_appbar_button
        self.menu.open()
    
    def menu_callback(self, text_item):
        self.menu.dismiss()
        self.manager.current = text_item

    # ações

    def do_like(self):
        self.check_like()
        if type(self.like_check_ob) is dict:          
            
            like_ob = AccessDB(name_url="likes", tag="LIKES")
            like_ob = like_ob.delete(id_object=self.like_check_ob["results"]["id"])
            if type(like_ob) is dict:
                self.ids.id_like.icon_color = (0, 0, 0, 1)
       

        else:
            data = {
                "user": self.manager.user_id,
                "annotation": self.manager.current_view_annotation
            }
            like_ob = AccessDB(name_url="likes/", tag="LIKES")
            like_ob = like_ob.post(data=data)
            if type(like_ob) is bool: # aqui tem que dar 201 status
                self.ids.id_like.icon_color = (1, 1, 0, 1)
            
        
    def do_favorite(self):
        self.check_favorite()
        if type(self.favorite_check_ob) is dict:          
            
            favorite_ob = AccessDB(name_url="favorites", tag="FAVORITES")
            favorite_ob = favorite_ob.delete(id_object=self.favorite_check_ob["results"]["id"])
            if type(favorite_ob) is dict:
                self.ids.id_favorite.icon_color = (0, 0, 0, 1)
       

        else:
            data = {
                "user": self.manager.user_id,
                "annotation": self.manager.current_view_annotation
            }
            favorite_ob = AccessDB(name_url="favorites/", tag="FAVORITES")
            favorite_ob = favorite_ob.post(data=data)
            if type(favorite_ob) is bool: # aqui tem que dar 201 status
                self.ids.id_favorite.icon_color = (1, 1, 0, 1)


    def check_like(self, *args):
        data = {
            "id": "",
            "user": self.manager.user_id,
            "annotation": self.manager.current_view_annotation
        }
        self.like_check_ob =  AccessDB(name_url="annotations/likes/check/", tag="LIKES_CHECK")
        self.like_check_ob = self.like_check_ob.post(data=data)
        if type(self.like_check_ob) is dict:
            self.ids.id_like.icon_color = (1, 1, 0, 1) 
        else:
            self.ids.id_like.icon_color = (0, 0, 0, 1)


    def check_favorite(self, *args):
        data = {
            "id": "",
            "user": self.manager.user_id,
            "annotation": self.manager.current_view_annotation
        }
        self.favorite_check_ob =  AccessDB(name_url="annotations/favorites/check/", tag="FAVORITES_CHECK")
        self.favorite_check_ob = self.favorite_check_ob.post(data=data)
        if type(self.favorite_check_ob) is dict:
            self.ids.id_favorite.icon_color = (1, 1, 0, 1) 
        else:
            self.ids.id_favorite.icon_color = (0, 0, 0, 1)

    def go_profile(self):
        self.manager.current_view_user = self.user_to_chat
        self.manager.current = "profile_name"


    # fim ações

    def voltar(self, window, key, *args):
        # esc tem o codigo 27
        if key == 27:
            self.manager.current = "diary_name"
            # print(self.manager.current)
            return True

        return False
        



class CustomSwiper(MDSwiperItem):
    image = StringProperty()


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''