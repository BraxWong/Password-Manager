from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton
from Database.LoginDetailsDB import LoginDetailsDB  

class LoginDetailsStorage(Screen):

    def __init__(self, **kwargs):
        super(LoginDetailsStorage,self).__init__(**kwargs)
        self.db = LoginDetailsDB()
        self.mainLayout = BoxLayout(orientation='vertical')
        self.topRowLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0))
        self.backButton = MDRaisedButton(text="Back", on_release=self.on_button_press)
        self.topRowLayout.add_widget(self.backButton)
        self.topRowLayout.add_widget(Label(text='Store Login Details', font_size='20sp', halign='center'))
        self.mainLayout.add_widget(self.topRowLayout)

        self.applicationNameLayout = BoxLayout(orientation='horizontal')
        self.applicationNameLayout.add_widget(Label(text='Name of Application/Website',
                                                    font_size='15sp',
                                                    pos_hint={'x':0.2,'y':0})
                                            )
        self.applicationNameTextInput = TextInput(text='', 
                                                  multiline=False,
                                                  size_hint=(None,None), 
                                                  height=30, 
                                                  width=250,
                                                  pos_hint={'x':0.5,'y':0.45})

        self.applicationNameLayout.add_widget(self.applicationNameTextInput)
        self.mainLayout.add_widget(self.applicationNameLayout)


        self.usernameLayout = BoxLayout(orientation='horizontal')
        self.usernameLayout.add_widget(Label(text='Username',
                                                    font_size='15sp',
                                                    pos_hint={'x':0.2,'y':0},))
        self.usernameTextInput = TextInput(text='', 
                                                  multiline=False,
                                                  size_hint=(None,None), 
                                                  height=30, 
                                                  width=250,
                                                  pos_hint={'x':0.5,'y':0.45})
        self.usernameLayout.add_widget(self.usernameTextInput)
        self.mainLayout.add_widget(self.usernameLayout)

        self.passwordLayout = BoxLayout(orientation='horizontal')
        self.passwordLayout.add_widget(Label(text='Password',
                                                    font_size='15sp',
                                                    pos_hint={'x':0.2,'y':0},))
        self.passwordTextInput = TextInput(text='', 
                                                  multiline=False,
                                                  size_hint=(None,None), 
                                                  height=30, 
                                                  width=250,
                                                  pos_hint={'x':0.5,'y':0.45})
        self.passwordLayout.add_widget(self.passwordTextInput)
        self.mainLayout.add_widget(self.passwordLayout)

        self.storeLoginDetailsButton = Button(text='Store Login Details',
                                             size_hint=(None,None),
                                             height=20,
                                             width=200,
                                             pos_hint={'x':0.379,'y':0.2})
        self.storeLoginDetailsButton.bind(on_press=self.storeLoginDetails)
        self.mainLayout.add_widget(self.storeLoginDetailsButton)
        self.add_widget(self.mainLayout)
       
    def on_button_press(self, instance_button: MDRaisedButton):
        self.manager.current = 'Menu Screen'

    def storeLoginDetails(self,widget): 
        if len(self.applicationNameTextInput.text) > 0 and len(self.usernameTextInput.text) > 0 and len(self.passwordTextInput.text) > 0:
            self.db.addEntryToDB(self.applicationNameTextInput.text,self.usernameTextInput.text,self.passwordTextInput.text) 
            popup = Popup(title='Password Stored',
                                    content=Label(text=f'Website:{self.applicationNameTextInput.text}\nUsername:{self.usernameTextInput.text}\nPassword:{self.passwordTextInput.text}\nSaved in Database'),
                                    size_hint=(None,None),
                                    size=(400,400))
            popup.open()
            self.applicationNameTextInput.text = ""
            self.usernameTextInput.text = ""
            self.passwordTextInput.text = ""
        else:
            errorMessage = "The following information is missing:"
            if len(self.applicationNameTextInput.text) <= 0:
                errorMessage += "\nApplication Name"
            if len(self.usernameTextInput.text) <= 0:
                errorMessage += "\nUsername"
            if len(self.passwordTextInput.text) <= 0:
                errorMessage += "\nPassword"
            popUp = Popup(title='Error',
                            content=Label(text=errorMessage),
                            size_hint=(None,None),
                            size=(400,400))
            popUp.open()

