from show_stuff import get_google_information, start_up, send_message, qr_code, get_google_calendar
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
from kivy.properties import ObjectProperty
import sys


class MenuScreen(Screen):
    pass

class SignIn(Screen):
    pass

class About_Us(Screen):
    pass

class Full_Image(Screen):
    def __init__(self, *args, **kwargs):
	super(Full_Image, self).__init__(*args, **kwargs)
	qr_code()
	#sleep(30)
   
class Dashboard(Screen):
    def __init__(self, **kwargs):
	self.alert = get_google_information()[0]
	(self.text, self.uname) = get_google_calendar()
	self.trigger = Clock.create_trigger(self.update_value, 30)
	super(Dashboard, self).__init__(**kwargs)

    def on_enter(self):
      	self.trigger()
 		
    def update_value(self, *args):
	self.alert = get_google_information()[0]	
	if self.alert:
		self.parent.current =  "Alert"
	else:
		self.trigger()
		(self.text, self.uname) = get_google_calendar()
    
		

class Alert(Screen):
    msg = ObjectProperty(None)
    def __init__(self, *args, **kwargs):
	(self.is_alert, self.msg, self.uname) = get_google_information()
	self.trigger = Clock.create_trigger(self.update_value, 30)
	super(Alert, self).__init__(*args, **kwargs)
    	 
    def on_enter(self):
	(self.is_alert, self.msg, self.uname) = get_google_information()
   	self.trigger()
 
    def update_value(self, *args):
        (self.is_alert, self.msg, self.uname) = get_google_information()
	self.ids['msg'].text = self.msg
	if not self.is_alert:
		#self.event.cancel() 
		self.parent.current = "Dashboard"
	else:
		self.trigger()



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

