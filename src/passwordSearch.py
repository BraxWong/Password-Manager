from kivy.uix.modalview import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from CustomWidget.BorderedLabel import BorderedLabel
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from Database.LoginDetailsDB import *

class PasswordSearch(Screen):
    def __init__(self, **kwargs):
        super(PasswordSearch,self).__init__(**kwargs)
        self.db = LoginDetailsDB()
        self.mainLayout = BoxLayout(orientation='vertical')
        self.mainLayout.add_widget(Label(text='Password Searching', font_size='20sp', size_hint_y=None, height=50))
        self.allPassword = self.db.fetchAllFromDB()

        self.data = [(password[0],password[1],password[2]) for password in self.allPassword]
        table = MDDataTable(
            column_data = [
                ("Application Name",dp(30)),
                ("Username",dp(30)),
                ("Password",dp(30))
            ],
            row_data = self.data,
            size_hint = (None,None),
            width = 800,
            height = 400,
            background_color_cell="#451938",
            background_color_selected_cell="e4514f",
            use_pagination = True
        )
        self.table_layout = AnchorLayout()
        self.table_layout.add_widget(table)
        self.mainLayout.add_widget(self.table_layout)
        self.add_widget(self.mainLayout)
