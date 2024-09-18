from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from Database.LoginDetailsDB import *

class Menu(GridLayout):
    #Establishes the UI of the Menu Screen
    #TODO: Have to create a callback functions for all the buttons to transition to a different screen
    def __init__(self, **kwargs):
        super(Menu,self).__init__(**kwargs)
        self.cols=1
        self.add_widget(Label(text='Password Manager',font_size='20sp'))
        self.searchPassword = Button(text='Find your password')
        self.searchPassword.bind(on_press=self.startDatabase)
        self.add_widget(self.searchPassword)
        self.storePassword = Button(text='Store a password')
        self.add_widget(self.storePassword)
        self.generatePassword = Button(text='Generate a password')
        self.add_widget(self.generatePassword)

    def startDatabase(self,widget):
        LoginDetailsDB()
