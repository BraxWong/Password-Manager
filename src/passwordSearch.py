from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from Database.LoginDetailsDB import *

class PasswordSearch(Screen):
    def __init__(self, **kwargs):
        super(PasswordSearch,self).__init__(**kwargs)
        self.db = LoginDetailsDB()
        self.mainLayout = BoxLayout(orientation='vertical')
        self.mainLayout.add_widget(Label(text='Password Searching', font_size='20sp'))
        self.allPassword = self.db.fetchAllFromDB()
