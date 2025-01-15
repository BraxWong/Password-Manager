from kivy.uix.modalview import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from Database.LoginDetailsDB import *
from Database.VerifyUserDB import *
from datetime import datetime

class PasswordSearch(Screen):
    def __init__(self, **kwargs):
        super(PasswordSearch,self).__init__(**kwargs)
        self.db = LoginDetailsDB() 
        self.verifyUserDB = VerifyUserDB()
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

        table_and_buttons = BoxLayout(orientation='vertical', size_hint=(None, None), width=800)
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
            check = True,
            use_pagination = True
        )
        self.table.bind(on_check_press=self.on_check_press)
        table_and_buttons.add_widget(self.table)
        table_and_buttons.add_widget(button_box)
        self.table_layout = AnchorLayout()
        self.table_layout.add_widget(table_and_buttons)
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
                "Delete": self.deleteLoginDetailsConfirmation,
                "Back": self.returnToMenu,
                "Reveal Password": self.revealPassword,
                "Hide Password": self.hidePassword
            }[instance_button.text]()
        except KeyError:
            pass

    def on_pre_enter(self, *args):
        if len(self.verifyUserDB.getUserPasswordAndHint()) > 0:
            self.passwordSearchLogin()
        else:
            self.createPasswordAndHint()

    def passwordSearchLogin(self):
        mainLayout = BoxLayout(orientation='vertical')
        passwordLayout = BoxLayout(orientation='horizontal')
        passwordLayout.add_widget(Label(text='Password',
                                                font_size='15sp',
                                                pos_hint={'x':0.2,'y':0})
                                            )
        passwordTextInput = TextInput(text='', 
                                      multiline=False,
                                      size_hint=(None,None), 
                                      height=30, 
                                      width=250,
                                      pos_hint={'x':0.5,'y':0.45})

        passwordLayout.add_widget(passwordTextInput)
        mainLayout.add_widget(passwordLayout)

        hintLayout = BoxLayout(orientation='horizontal')
        hintLayout.add_widget(Label(text='Hint',
                                        font_size='15sp',
                                        pos_hint={'x':0.2,'y':0},))
        hintTextInput = TextInput(text='', 
                                  multiline=False,
                                  size_hint=(None,None), 
                                  height=30, 
                                  width=250,
                                  pos_hint={'x':0.5,'y':0.45})
        hintLayout.add_widget(hintTextInput)
        mainLayout.add_widget(hintLayout)

        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        confirmButton = MDRaisedButton(text='Confirm')
        hintButton = MDRaisedButton(text='Hint')
        button_box.add_widget(confirmButton)
        button_box.add_widget(hintButton)
        mainLayout.add_widget(button_box)
        popUp = Popup(title='Password Search Login',
                          content=mainLayout,
                          size_hint=(None,None),
                          size=(600,600))
        hintButton.bind(on_release=lambda x:self.showHint(x,hintTextInput))
        confirmButton.bind(on_release=lambda x:self.verifyPasswordSearchLogin(x,passwordTextInput.text,popUp))
        popUp.open()
    

    def showHint(self, instance, textBox):
        hint = self.verifyUserDB.getUserPasswordAndHint()[0][1]
        textBox.text = hint

    def verifyPasswordSearchLogin(self,instance,userInputPassword,passwordPopup):
        password = self.verifyUserDB.getUserPasswordAndHint()[0][0]
        if password == userInputPassword:
            self.refresh_table_data()
            passwordPopup.dismiss()
        else:
            incorrectPasswordPopUp = Popup(title='Incorrect Password',
                                           content=Label(text='Incorrect Password'),
                                           size_hint=(None,None),
                                           size=(600,600))
            incorrectPasswordPopUp.open()


    
    def createPasswordAndHint(self):
        mainLayout = BoxLayout(orientation='vertical')
        passwordLayout = BoxLayout(orientation='horizontal')
        passwordLayout.add_widget(Label(text='Password',
                                                font_size='15sp',
                                                pos_hint={'x':0.2,'y':0})
                                            )
        passwordTextInput = TextInput(text='', 
                                      multiline=False,
                                      size_hint=(None,None), 
                                      height=30, 
                                      width=250,
                                      pos_hint={'x':0.5,'y':0.45})

        passwordLayout.add_widget(passwordTextInput)
        mainLayout.add_widget(passwordLayout)

        hintLayout = BoxLayout(orientation='horizontal')
        hintLayout.add_widget(Label(text='Hint',
                                        font_size='15sp',
                                        pos_hint={'x':0.2,'y':0},))
        hintTextInput = TextInput(text='', 
                                  multiline=False,
                                  size_hint=(None,None), 
                                  height=30, 
                                  width=250,
                                  pos_hint={'x':0.5,'y':0.45})
        hintLayout.add_widget(hintTextInput)
        mainLayout.add_widget(hintLayout)

        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        confirmButton = MDRaisedButton(text='Confirm')
        cancelButton = MDRaisedButton(text='Cancel')
        button_box.add_widget(confirmButton)
        button_box.add_widget(cancelButton)
        mainLayout.add_widget(button_box)
        popUp = Popup(title='Create password & hint',
                          content=mainLayout,
                          size_hint=(None,None),
                          size=(600,600))
        cancelButton.bind(on_release=lambda x:self.cancelPasswordAndHint(x,popUp))
        confirmButton.bind(on_release=lambda x:self.createPasswordSearchPassword(x,passwordTextInput.text,hintTextInput.text,popUp))
        popUp.open()
        
    def createPasswordSearchPassword(self,instance,password,hint,popUp):
        self.verifyUserDB.addPasswordAndHint(password,hint)
        popUp.dismiss()

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

    def cancelPasswordAndHint(self,instance,popUp):
        popUp.dismiss()
        self.returnToMenu()

    def returnToMenu(self):
        self.manager.current = 'Menu Screen'

    def updateLoginDetails(self):
        if len(self.table.get_row_checks()) > 1:
            popUp = Popup(title='Error',
                          content=Label(text="Please only select 1 row at a time when updating your login details"),
                          size_hint=(None,None),
                          size=(600,600))
            popUp.open()
        else:
            currentIndex = int(self.rowChecked[0])
            mainLayout = BoxLayout(orientation='vertical')
            applicationNameLayout = BoxLayout(orientation='horizontal')
            applicationNameLayout.add_widget(Label(text='Name of Application/Website',
                                                   font_size='15sp',
                                                   pos_hint={'x':0.2,'y':0})
                                             )
            applicationNameTextInput = TextInput(text='', 
                                                    multiline=False,
                                                    size_hint=(None,None), 
                                                    height=30, 
                                                    width=250,
                                                    pos_hint={'x':0.5,'y':0.45})
            applicationNameTextInput.text = self.table.row_data[currentIndex][2]

            applicationNameLayout.add_widget(applicationNameTextInput)
            mainLayout.add_widget(applicationNameLayout)

            usernameLayout = BoxLayout(orientation='horizontal')
            usernameLayout.add_widget(Label(text='Username',
                                            font_size='15sp',
                                            pos_hint={'x':0.2,'y':0},))
            usernameTextInput = TextInput(text='', 
                                          multiline=False,
                                          size_hint=(None,None), 
                                          height=30, 
                                          width=250,
                                          pos_hint={'x':0.5,'y':0.45})
            usernameTextInput.text = self.table.row_data[currentIndex][3]
            usernameLayout.add_widget(usernameTextInput)
            mainLayout.add_widget(usernameLayout)

            passwordLayout = BoxLayout(orientation='horizontal')
            passwordLayout.add_widget(Label(text='Password',
                                            font_size='15sp',
                                            pos_hint={'x':0.2,'y':0},))
            passwordTextInput = TextInput(text='', 
                                          multiline=False,
                                          size_hint=(None,None), 
                                          height=30, 
                                          width=250,
                                          pos_hint={'x':0.5,'y':0.45})
            passwordTextInput.text = self.allPassword[currentIndex]
            passwordLayout.add_widget(passwordTextInput)
            mainLayout.add_widget(passwordLayout)

            button_box = MDBoxLayout(
                pos_hint={"center_x": 0.5},
                adaptive_size=True,
                padding="24dp",
                spacing="24dp",
            )

            confirmButton = MDRaisedButton(text='Confirm')
            cancelButton = MDRaisedButton(text='Cancel')
            button_box.add_widget(confirmButton)
            button_box.add_widget(cancelButton)
            mainLayout.add_widget(button_box)
            editLoginDetailsPopup = Popup(title='Edit Login Details',
                                          content=mainLayout,
                                          size_hint=(None,None),
                                          size=(600,600))

            cancelButton.bind(on_release=editLoginDetailsPopup.dismiss)
            confirmButton.bind(on_release=lambda x:self.updateLoginDetailsToDB(x,editLoginDetailsPopup,applicationNameTextInput.text,usernameTextInput.text,passwordTextInput.text))
            editLoginDetailsPopup.open()

    def updateLoginDetailsToDB(self,instance,popup,applicationName,username,password):
        self.db.updateEntryToDB(applicationName,username,password)
        self.refresh_table_data()
        popup.dismiss()
        updatePopup = Popup(title='Success',
                            content=Label(text='Your details have been updated'),
                            size_hint=(None,None),
                            size=(600,600))
        updatePopup.open()

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

    def deleteLoginDetailsConfirmation(self):
        confirmationLayout = BoxLayout(orientation='vertical',
                                               size_hint=(None,None),
                                               width=500,
                                               pos_hint={'center_x':0.5})
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        confirmButton = MDRaisedButton(text='Confirm')
        cancelButton = MDRaisedButton(text='Cancel')
        confirmationLayout.add_widget(Label(text='Are you sure you want to remove these login details?'))
        button_box.add_widget(confirmButton)
        button_box.add_widget(cancelButton)
        confirmationLayout.add_widget(button_box)
        confirmationPopUp = Popup(title='Confirmation',
                                  content=confirmationLayout,
                                  size_hint=(None,None),
                                  size=(600,200))

        cancelButton.bind(on_release=confirmationPopUp.dismiss)
        confirmButton.bind(on_release=lambda x: self.deleteLoginDetails(x,confirmationPopUp))
        confirmationPopUp.open()

        
    def deleteLoginDetails(self, instance, popupWindow):
        popupWindow.dismiss()
        message = "The following website login details have been removed:"
        rows_to_delete = [] 
        for row in self.rowChecked:
            rows_to_delete.append(self.table.row_data[int(row)])

        rows_to_delete.sort(key=lambda x: int(x[0]), reverse=True)

        for row in rows_to_delete:
            self.db.removeEntryFromDB(row[2])
            self.table.remove_row(self.table.row_data[int(row[0])])
            message += f"\n{row[2]}"

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
