from show_stuff import get_google_information, start_up, send_message, qr_code
from time import sleep
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.image import Image
import sys


class MenuScreen(Screen):
    pass

class SignIn(Screen):
    pass

class About_Us(Screen):
    pass

class Full_Image(Screen):
    qr_code()
    

class Dashboard(Screen):
    def __init__(self, *args, **kwargs):
	super(Dashboard, self).__init__(*args, **kwargs)
	(self.text, self.uname) = get_google_information()

    def update_value(self):
		self.text = get_google_information()
		if not self.text[1]:
			self.manager.current = "Alert"
    
		

class Alert(Screen):
    def __init__(self, *args, **kwargs):
	super(Alert, self).__init__(*args, **kwargs)
	(self.text, self.uname) = get_google_information()

    def update_value(self):
		self.text = get_google_information()
		if self.text[1]:
			self.manager.current = "Dashboard"



buildKV = Builder.load_file("office_manager.kv")

"""
class change_text(Widget):
	def __init__(self, **kwargs):
        	super(YourWidget, self).__init__(**kwargs)
		self.text = get_google_information()

	def update_text():
		self.text = get_google_information()
"""

class office_manager(App):
	icon = "icon1.png"
	title = "Office Manager"
	def build(self):
		#Clock.schedule_interval(Dashboard().update_value(), 20/1.)
		return buildKV



	

	

if __name__ == '__main__':
	office_manager().run() 

