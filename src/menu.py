from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from Database.LoginDetailsDB import *
from passwordGeneration import *

class Menu(Screen):
    #Establishes the UI of the Menu Screen
    #TODO: Have to create a callback functions for all the buttons to transition to a different screen
    def __init__(self, **kwargs):
        super(Menu,self).__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.cols=1

        self.layout.add_widget(Label(text='Password Manager',font_size='20sp'))

        self.searchPassword = Button(text='Find your password')
        self.searchPassword.bind(on_press=self.startDatabase)
        self.layout.add_widget(self.searchPassword)

        self.storePassword = Button(text='Store a password')
        self.layout.add_widget(self.storePassword)

        self.generatePassword = Button(text='Generate a password')
        self.generatePassword.bind(on_press=self.startPasswordGeneration)
        self.layout.add_widget(self.generatePassword)
        
        self.add_widget(self.layout)

    #TODO: The database does not work yet as mySQL will be needed to installed on the local machine
    def startDatabase(self,widget):
        LoginDetailsDB()

    def startPasswordGeneration(self,widget):
        self.manager.current = 'Password Generation Screen'
