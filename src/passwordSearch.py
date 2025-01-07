from kivy.uix.modalview import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from Database.LoginDetailsDB import *

class PasswordSearch(Screen):
    def __init__(self, **kwargs):
        super(PasswordSearch,self).__init__(**kwargs)
        self.db = LoginDetailsDB()
        self.mainLayout = BoxLayout(orientation='vertical',padding=20, spacing=10)
        self.topRowLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0))
        self.backButton = MDRaisedButton(text="Back", on_release=self.on_button_press)
        self.topRowLayout.add_widget(self.backButton)
        self.topRowLayout.add_widget(Label(text='Password Searching', font_size='20sp', halign='center'))        
        self.mainLayout.add_widget(self.topRowLayout)
        self.allPassword = self.db.fetchAllFromDB()

        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        for button_text in ["Delete", "Update"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )
        self.data = [(i, *password[:4]) for i,password in enumerate(self.allPassword)]
        self.table = MDDataTable(
            column_data = [
                ("Index",dp(30)),
                ("Application Name",dp(30)),
                ("Username",dp(30)),
                ("Password",dp(30)),
                ("Date Created",dp(30))
            ],
            row_data = self.data,
            size_hint = (None,None),
            width = 800,
            height = 400,
            background_color_cell="#451938",
            background_color_selected_cell="e4514f",
            use_pagination = True,
            check = True
        )
        self.table_layout = AnchorLayout()
        self.table_layout.add_widget(self.table)
        self.mainLayout.add_widget(button_box)
        self.mainLayout.add_widget(self.table_layout)
        self.add_widget(self.mainLayout)

    def on_button_press(self, instance_button: MDRaisedButton):
        try:
            {
                "Update": self.updateLoginDetails,
                "Delete": self.deleteLoginDetails,
                "Back": self.returnToMenu
            }[instance_button.text]()
        except KeyError:
            pass

    def on_pre_enter(self, *args):
        self.refresh_table_data()

    def refresh_table_data(self):
        self.allPassword = self.db.fetchAllFromDB()
        self.data = [(i, *password[:4]) for i, password in enumerate(self.allPassword)]
        self.table.update_row_data(self.table.row_data, self.data)

    def returnToMenu(self):
        self.manager.current = 'Menu Screen'

    def updateLoginDetails(self):
        if len(self.table.get_row_checks()) > 1:
            popUp = Popup(title='Error',
                          content=Label(text="Please only select 1 row at a time when updating your login details"),
                          size_hint=(None,None),
                          size=(600,600))
            popUp.open()

# ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
# ┃                                                                              ┃
# ┃      TODO: Might want to ask for confirmation before deleting the login      ┃
# ┃                              details for real.                               ┃
# ┃                                                                              ┃
# ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
    def deleteLoginDetails(self):
        message = "The following website login details have been removed:"
        rows_to_delete = self.table.get_row_checks()
    
        rows_to_delete.sort(key=lambda x: int(x[0]), reverse=True)
        
        for row in rows_to_delete:
            self.db.removeEntryFromDB(row[1])
            self.table.remove_row(self.table.row_data[int(row[0])])
            message += f"\n{row[1]}"
            
        popUp = Popup(title='Success',
                    content=Label(text=message),
                    size_hint=(None,None),
                    size=(600,600))
        popUp.open() 
