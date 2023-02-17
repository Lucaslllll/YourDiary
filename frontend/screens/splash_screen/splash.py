from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kaki.app import App
import os
os.environ['KIVY_IMAGE'] = 'sdl2,gif'

class Splash(MDScreen):
	
	def on_pre_enter(self):
		Clock.schedule_once(self.change_screen, 30)

	def change_screen(self, *args):
		self.manager.current = self.manager.current_atual