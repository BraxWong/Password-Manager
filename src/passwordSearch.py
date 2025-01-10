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
from datetime import datetime

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
        self.allLoginDetails = self.db.fetchAllFromDB()

        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        for button_text in ["Delete", "Update", "Reveal Password", "Hide Password"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )

        self.rowChecked = []
        self.data = []
        self.allPassword = []
        self.table = MDDataTable(
            column_data = [
                ("Index",dp(30)),
                ("Password Safety",dp(30)),
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
        self.table.bind(on_check_press=self.on_check_press)
        self.table_layout = AnchorLayout()
        self.table_layout.add_widget(self.table)
        self.mainLayout.add_widget(button_box)
        self.mainLayout.add_widget(self.table_layout)
        self.add_widget(self.mainLayout)

    def on_check_press(self, instance_table, current_row):
        if current_row[0] not in self.rowChecked:
            self.rowChecked.append(current_row[0])
        else:
            self.rowChecked.remove(current_row[0])

    def on_button_press(self, instance_button: MDRaisedButton):
        try:
            {
                "Update": self.updateLoginDetails,
                "Delete": self.deleteLoginDetails,
                "Back": self.returnToMenu,
                "Reveal Password": self.revealPassword,
                "Hide Password": self.hidePassword
            }[instance_button.text]()
        except KeyError:
            pass

    def on_pre_enter(self, *args):
        self.refresh_table_data()

    def refresh_table_data(self):
        self.allLoginDetails = self.db.fetchAllFromDB()
        self.data = []
        self.allPassword = []
        if len(self.allLoginDetails) > 0:
            for i,password in enumerate(self.allLoginDetails):
                self.allPassword.append(password[2])
                self.password = "*" * len(password[2])
                self.data.append((i,self.dateComparison(password[3]),password[0],password[1],self.password,password[3]))
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

    def revealPassword(self):
        for row in self.rowChecked: 
            currentIndex = int(row)
            newRow = list(self.table.row_data[currentIndex])
            newRow[4] = self.allPassword[currentIndex]
            self.table.update_row(self.table.row_data[currentIndex],newRow)

    def hidePassword(self):
        for row in self.rowChecked:
            currentIndex = int(row)
            newRow = list(self.table.row_data[currentIndex])
            newRow[4] = "*" * len(self.allPassword[currentIndex])
            self.table.update_row(self.table.row_data[currentIndex],newRow)

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

    def dateComparison(self,date):
        self.todays_date = datetime.now().date()         
        date_format = '%Y-%m-%d'
        date = datetime.strptime(date,date_format).date()
        difference = (self.todays_date - date).days
        if difference < 15:
            return ("checkbox-marked-circle",[39/256,174/256,96/256,1],"Safe")
        elif difference > 15 and difference < 30:
            return ("alert",[39/256,174/256,96/256,1],"Caution")
        else:
            return ("alert-circle",[39/256,174/256,96/256,1],"Danger")
