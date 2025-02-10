from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton
from Database.LoginDetailsDB import LoginDetailsDB  
import Util.Util

class PasswordGeneration(Screen):

    def __init__(self, **kwargs):
        super(PasswordGeneration, self).__init__(**kwargs)
        self.db = LoginDetailsDB() 
        self.mainLayout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),  
            padding=0,
            spacing=50  
        )

        self.topRowLayout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',  
            padding=(10, 0)  
        )

        self.backButton = MDRaisedButton(text="Back", on_release=self.on_button_press)
        self.topRowLayout.add_widget(self.backButton)

        self.topRowLayout.add_widget(
            Label(
                text='Create a Password',
                font_size='20sp',
                halign='center',
                size_hint_x=0.8
            )
        )

        self.mainLayout.add_widget(self.topRowLayout)

        self.applicationNameLayout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )
        self.applicationNameLayout.add_widget(
            Label(
                text='Name of application/website',
                font_size='15sp',
                size_hint_x=0.4
            )
        )
        self.applicationNameTextInput = TextInput(
            text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.applicationNameLayout.add_widget(self.applicationNameTextInput)
        self.mainLayout.add_widget(self.applicationNameLayout)

                
        self.usernameLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        self.usernameLayout.add_widget(
             Label(text='Username', font_size='15sp', size_hint_x=0.4)
        )
        self.usernameTextInput = TextInput(
             text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.usernameLayout.add_widget(self.usernameTextInput)
        self.mainLayout.add_widget(self.usernameLayout)

        self.passwordLengthLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp', spacing='10dp')
        self.passwordLengthLayout.add_widget(
            Label(text='Length of password', font_size='15sp', size_hint_x=0.4)
        )
        self.passwordSliderLayout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        self.passwordLengthLabel = Label(text='14', font_size='20sp', halign='center')
        self.passwordSliderLayout.add_widget(self.passwordLengthLabel)
        self.passwordLengthSlider = Slider(
            min=1, max=64, value=14, value_track=True, value_track_color=[1, 0, 0, 1]
        )
        self.passwordLengthSlider.bind(value=self.onSliderValueChange)
        self.passwordSliderLayout.add_widget(self.passwordLengthSlider)
        self.passwordLengthLayout.add_widget(self.passwordSliderLayout)
        self.mainLayout.add_widget(self.passwordLengthLayout)

        self.symbolLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        self.symbolLayout.add_widget(
            Label(text='Include special symbol', font_size='15sp', size_hint_x=0.135)
        )
        self.symbolEnabledCheckBox = CheckBox(size_hint_x=0.2)
        self.symbolLayout.add_widget(self.symbolEnabledCheckBox)
        self.mainLayout.add_widget(self.symbolLayout)

        self.generatePasswordButton = Button(
            text='Generate a password', size_hint=(None, None), height='40dp', width='200dp', pos_hint={'center_x': 0.5}
        )
        self.generatePasswordButton.bind(on_press=self.updateLoginDetailsToDB)
        self.mainLayout.add_widget(self.generatePasswordButton)
       
        self.mainLayout.add_widget(Widget(size_hint_y=1))
        
        self.add_widget(self.mainLayout)

    def onSliderValueChange(self,widget,val):
        self.passwordLengthLabel.text=str(int(val))

    def on_button_press(self, instance_button: MDRaisedButton):
        self.manager.current = 'Menu Screen'

    def updateLoginDetailsToDB(self,widget):
        if not self.checkLoginDetails():
            password = Util.Util.generatePassword(self.symbolEnabledCheckBox.active, int(self.passwordLengthLabel.text))
            self.db.addEntryToDB(self.applicationNameTextInput.text,self.usernameTextInput.text,password)
            popup = Popup(title='Password Generated',
                            content=Label(text=f'Website:{self.applicationNameTextInput.text}\nUsername:{self.usernameTextInput.text}\nPassword:{password}\nSaved in Database'),
                            size_hint=(None,None),
                            size=(400,400))
            popup.open()
            self.resetInputWidgetValue()
            return password

    def checkLoginDetails(self):
        missingInformation = False
        errorMessage = "Please provide the following information:\n"
        if self.applicationNameTextInput.text == "":
            errorMessage += "Name of the Application\n"
            missingInformation = True
        if self.usernameTextInput.text == "":
            errorMessage += "Your Username"
            missingInformation = True
        if missingInformation:
            popup = Popup(title='Error',
                        content=Label(text=errorMessage),
                        size_hint=(None,None),
                        size=(400,400))
            popup.open()
        return missingInformation

    def resetInputWidgetValue(self):
        self.applicationNameTextInput.text = ''
        self.usernameTextInput.text = ''
        self.passwordLengthLabel.text = '14'
        self.symbolEnabledCheckBox.active = False
        self.passwordLengthSlider.value = 14