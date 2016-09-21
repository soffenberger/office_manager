from show_stuff import get_google_information, start_up, send_message, qr_code, get_google_calendar, store_phone_number, get_phone_number
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
    def __init__(self, *args, **kwargs):
        self.number = "Nothing yet"
        self.trigger = Clock.create_trigger(self.update_value, 10) 
        super(SignIn, self).__init__(*args, **kwargs)

    def on_enter(self):
        self.trigger()

    def update_value(self, *args):
        self.number = get_phone_number()
        if self.number == "Nothing Yet":
            self.trigger()
        self.ids['msg'].text = self.number

    def leave(self, *args):
        store_phone_number(self.number)
        self.parent.current =  "Menu"
    
    def refresh(self, *args):
        self.trigger()


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
        self.days=["mon","tues","wed","thurs","fri"]
        (self.text, self.uname) = get_google_calendar()
        self.trigger1 = Clock.create_trigger(self.update_value, .0001)
        self.trigger = Clock.create_trigger(self.update_value, 30)
        super(Dashboard, self).__init__(**kwargs)

    def on_enter(self):
        self.trigger1()
        
    def update_value(self, *args):
        self.alert = get_google_information()[0]    
        if self.alert:
            self.parent.current =  "Alert"
        else:
            self.trigger()
            (self.text, self.uname) = get_google_calendar()
            for i in range(5):
                self.ids['{0}'.format(self.days[i])].width = 5
                try:
                    if len(self.text[i]) == 1:
                        self.ids['{0}1'.format(self.days[i])].text = self.text[i][0]
                        self.ids['{0}_lay'.format(self.days[i])].remove_widget(self.ids['{0}2'.format(self.days[i])])
                        self.ids['{0}_lay'.format(self.days[i])].remove_widget(self.ids['{0}3'.format(self.days[i])])  
                    elif len(self.text[i]) == 2:
                        self.ids['{0}1'.format(self.days[i])].text = self.text[i][0]
                        self.ids['{0}2'.format(self.days[i])].text = self.text[i][1]
                        self.ids['{0}_lay'.format(self.days[i])].remove_widget(self.ids['{0}3'.format(self.days[i])]) 
                    elif len(self.text[i]) == 3:
                        self.ids['{0}1'.format(self.days[i])].text = self.text[i][0]
                        self.ids['{0}2'.format(self.days[i])].text = self.text[i][1]
                        self.ids['{0}3'.format(self.days[i])].text = self.text[i][2]
                except ReferenceError:
                    pass

class Alert(Screen):
    def __init__(self, *args, **kwargs):
        (self.is_alert, self.msg, self.uname) = get_google_information()
        self.trigger = Clock.create_trigger(self.update_value, 30)
        super(Alert, self).__init__(*args, **kwargs)
         
    def on_enter(self):
        (self.is_alert, self.msg, self.uname) = get_google_information()
        print(self.msg)
        self.ids['almsg'].text = self.msg
        self.trigger()
 
    def update_value(self, *args):
        (self.is_alert, self.msg, self.uname) = get_google_information()
        print(self.msg)
        self.ids['almsg'].text = self.msg
        if not self.is_alert:
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
    icon = "images/misc/icon2.png"
    title = "Office Manager"
    def build(self):
        #Clock.schedule_interval(Dashboard().update_value(), 20/1.)
        return buildKV



    

    

if __name__ == '__main__':
    office_manager().run() 

