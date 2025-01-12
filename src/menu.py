from kivy.lang import Builder
from kivy.core import text
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from Database.LoginDetailsDB import *
from importPassword import ImportPassword
from exportPassword import ExportPassword
from passwordGeneration import *
from loginDetailsStorage import * 

class Menu(Screen):
    #Establishes the UI of the Menu Screen
    #TODO: Have to create a callback functions for all the buttons to transition to a different screen
    def __init__(self, **kwargs):
        super(Menu,self).__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.cols=1
        self.layout.add_widget(Label(text='Password Manager',font_size='20sp'))

        self.searchPassword = Button(text='Find your password')
        self.searchPassword.bind(on_press=self.startPasswordSearch)
        self.layout.add_widget(self.searchPassword)

        self.storeUserDetails = Button(text='Store Login Details')
        self.storeUserDetails.bind(on_press=self.storeLoginDetails)
        self.layout.add_widget(self.storeUserDetails)

        self.generatePassword = Button(text='Generate a password')
        self.generatePassword.bind(on_press=self.startPasswordGeneration)
        self.layout.add_widget(self.generatePassword)

        self.importPassword = Button(text='Import password to system')
        self.importPassword.bind(on_press=self.importPasswordToSystem)
        self.layout.add_widget(self.importPassword)

        self.outputPassword = Button(text='Output password to file')
        self.outputPassword.bind(on_press=self.exportPasswordToTXT)
        self.layout.add_widget(self.outputPassword)
        
        self.add_widget(self.layout)

    def startPasswordSearch(self,widget):
        self.manager.current = 'Password Search Screen'

    def startPasswordGeneration(self,widget):
        self.manager.current = 'Password Generation Screen'

    def importPasswordToSystem(self,widget):
        self.importPassword = ImportPassword()

    def exportPasswordToTXT(self,widget):
        self.exportPassword = ExportPassword()

    def storeLoginDetails(self,widget):
        self.manager.current = 'Login Details Storage Screen'
