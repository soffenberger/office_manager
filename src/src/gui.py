from office_manager import get_google_information, start_up, send_message, qr_code, get_google_calendar, store_phone_number, get_phone_number
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
from kivy.core.window import Window
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
            self.parent.current =  "Menu"     

    def leave(self, *args):
        store_phone_number(self.number)
        
    
    def refresh(self, *args):
        self.trigger()



class About_Us(Screen):
    pass

class Set_Up_Phone(Screen):
    pass

class Set_Up_Calendar(Screen): 
    def __init__(self, *args, **kwargs):
        self.trigger2 = Clock.create_trigger(self.update, .3) 
        super(Set_Up_Calendar, self).__init__(*args, **kwargs)

    def on_enter(self):
        self.trigger2() 
     
    def update(self, *args):
        try:
            get_google_calendar()
            self.change()   
        except ValueError:
            self.trigger2()
    def change(self, *args):
        self.parent.current = "Dashboard"
            

class Full_Image(Screen):
    def __init__(self, *args, **kwargs):
        super(Full_Image, self).__init__(*args, **kwargs)
        qr_code()
 
class Dashboard(Screen): 
    def __init__(self, **kwargs):
        self.days=["mon","tues","wed","thurs","fri"]
        try:
            (self.text, self.uname, self.issetup) = get_google_calendar()
        except ValueError:
            (self.text, self.uname, self.issetup) = ("","","") 
        try:
            self.alert = get_google_information()[0]
        except SystemError:
            self.alert = ""
        self.trigger1 = Clock.create_trigger(self.update_value, .001)
        self.trigger = Clock.create_trigger(self.update_value, 10)
        super(Dashboard, self).__init__(**kwargs)

    def on_enter(self):
        self.trigger1()
        
    def update_value(self, *args): 
        try:
            self.alert = get_google_information()[0]
            if self.alert:
                self.parent.current =  "Alert"
            else:
                (self.text, self.uname, self.issetup) = get_google_calendar()
                self.trigger()
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
        except ValueError:
            self.parent.current =  "Set_Up_Calendar"
        except SystemError:
            self.parent.current = "Set_Up_Phone"

         
class Alert(Screen):
    def __init__(self, *args, **kwargs):
        try:
            (self.is_alert, self.msg, self.uname) = get_google_information()
        except SystemError:
            (self.is_alert, self.msg, self.uname) = ("","","") 
        self.trigger = Clock.create_trigger(self.update_value, 30)
        super(Alert, self).__init__(*args, **kwargs)
         
    def on_enter(self):
        try:
            (self.is_alert, self.msg, self.uname) = get_google_information()
            self.ids['almsg'].text = self.msg
            self.trigger()
        except SystemError:
            self.parent.current =  "Set_Up_Phone"
 
    def update_value(self, *args):
        try:
            (self.is_alert, self.msg, self.uname) = get_google_information()
            self.ids['almsg'].text = self.msg
            self.trigger()
            if not self.is_alert:
                self.parent.current = "Dashboard"
            else:
                self.trigger()
        except SystemError:
            self.parent.current =  "Set_Up_Phone"
        



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
    Window.size = (800,480)
    try:
        if int(sys.argv[1]) == 1:
            Window.fullscreen =1
    except IndexError:
        pass
    def build(self):
        #Clock.schedule_interval(Dashboard().update_value(), 20/1.)
        return buildKV



    

    

if __name__ == '__main__':
    office_manager().run() 

