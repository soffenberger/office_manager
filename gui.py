from show_stuff import get_google_information, start_up, send_message
from time import sleep
import kivy
kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


class home(Screen):
	def on_send(button_object):
		send_message()
		
		
	def draw():
		(message, color) = get_google_information()
		return (message,color)

	def refresh(interval_object):
		(message, color) = get_google_information()
		
	pass


class office_manager(App):
	icon = "icon1.png"
	title = "Office Manager"

	def build(self):
		return home()


	
def main():
	office_manager().run()

if __name__ == '__main__':
	main() 

