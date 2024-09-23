from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
class PasswordGeneration(Screen):

    def __init__(self, **kwargs):
        super(PasswordGeneration,self).__init__(**kwargs)
        self.layout = GridLayout(cols=2)
        self.layout.add_widget(Label(text='Create a Password',font_size='20sp'))
        self.layout.add_widget(Label(text='Name of applcation/website',font_size='15sp'))
        self.add_widget(self.layout)

