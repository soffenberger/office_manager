from show_stuff import get_google_information, start_up, send_message
from time import sleep
import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget


def on_send():
	send_message()
	
	
def draw():
	(message, color) = get_google_information()


def refresh():
	(message, color) = get_google_information()

class home(GridLayout):
	def __init__(self, **kwargs):
        	super(home, self).__init__(**kwargs)
        	self.cols = 6
        	self.row = 2
        	self.sendmess = Button(text="Leave Message")
        	self.hello.bind(on_press=self.auth)
        	self.add_widget(self.hello)



class MyApp(App):
	icon = "icon1.png"
	title = "Office Manager"

	def build(self):
		return home()

	def on_start(self):
		pass

	def on_stop(self):
		pass

	
def main():
	MyApp().run()

if __name__ == '__main__':
	main() 

