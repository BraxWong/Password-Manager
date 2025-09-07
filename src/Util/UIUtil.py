from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton
from Database.EmailSettings import TwoFactorAuthenticationSettingsDB
from Util.two_factor_authentication import *
from Util.Util import *
import threading
from kivy.clock import Clock

def create2FAPopupLayout(callback):
    two_factor_auth_db = TwoFactorAuthenticationSettingsDB()
    two_factor_auth_info = two_factor_auth_db.fetchAllFromDB()
    contact_info = two_factor_auth_info[0][0] 

    main_layout = BoxLayout(
        orientation='vertical',
        size_hint=(1, 1),  
        padding=0,
        spacing=50 
    )

    top_row_layout = BoxLayout(orientation='horizontal', 
                                size_hint_y=None, 
                                height=50, 
                                padding=(10, 0))
    top_row_layout.add_widget(
        Label(
            text='2FA', 
            font_size='20sp', 
            halign='center',
            size_hint_x=0.8
        )
    )        
    main_layout.add_widget(top_row_layout)

    two_factor_auth_layout = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height='50dp',
        spacing='10dp'
    )
    two_factor_auth_layout.add_widget(
        Label(
            text='Please enter your 2FA code',
            font_size='15sp',
            size_hint_x=0.4
        )
    )
    two_factor_auth_text_input = TextInput(
        text='', multiline=False, size_hint=(0.6, None), height='40dp'
    )
    two_factor_auth_layout.add_widget(two_factor_auth_text_input)
    main_layout.add_widget(two_factor_auth_layout)

    popUp = Popup(title='2FA',
                  content=main_layout,
                  size_hint=(None, None),
                  size=(600, 600))

    auth_system = None

    def send_2fa_code():
        nonlocal auth_system  
        auth_system = twoFactorAuth(contact_info)  
        Clock.schedule_once(lambda dt: print("2FA code sent!"), 0)  

    threading.Thread(target=send_2fa_code).start()

    def on_submit(instance):
        check_2FA_code(two_factor_auth_text_input.text, auth_system, popUp, callback)

    submit_button = MDRaisedButton(
        text="Submit",
        size_hint=(None, None),  
        size=(200, 50),          
        on_release=on_submit,
        pos_hint={'center_x': 0.5}
    )
    main_layout.add_widget(submit_button)
    popUp.open()

def show_incorrect_2FA_popup():
    popUp = Popup(title='Error',
                  content=Label(text="The 2FA code you provided is incorrect.Please try again."),
                  size_hint=(None,None),
                  size=(400,400))
    popUp.open() 

def createLoginDetailPopupLayout():
    mainLayout = BoxLayout(
                orientation='vertical',
                size_hint=(1, 1),  
                padding=0,
                spacing=50 
            )
    applicationNameLayout = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height='50dp',
        spacing='10dp'
    )
    applicationNameLayout.add_widget(
        Label(
            text='Name of application/website',
            font_size='15sp',
            size_hint_x=0.4
        )
    )
    applicationNameTextInput = TextInput(
        text='', multiline=False, size_hint=(0.6, None), height='40dp'
    )
    applicationNameLayout.add_widget(applicationNameTextInput)
    mainLayout.add_widget(applicationNameLayout)

            
    usernameLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
    usernameLayout.add_widget(
        Label(text='Username', font_size='15sp', size_hint_x=0.4)
    )
    usernameTextInput = TextInput(
        text='', multiline=False, size_hint=(0.6, None), height='40dp'
    )
    usernameLayout.add_widget(usernameTextInput)
    mainLayout.add_widget(usernameLayout)

    passwordLengthLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp', spacing='10dp')
    passwordLengthLayout.add_widget(
        Label(text='Length of password', font_size='15sp', size_hint_x=0.4)
    )
    passwordSliderLayout = BoxLayout(orientation='vertical', size_hint_x=0.6)
    passwordLengthLabel = Label(text='14', font_size='20sp', halign='center')
    passwordSliderLayout.add_widget(passwordLengthLabel)
    passwordLengthSlider = Slider(
        min=1, max=64, value=14, value_track=True, value_track_color=[1, 0, 0, 1]
    )
    passwordLengthSlider.bind(value=lambda instance, value:onSliderValueChange(value,passwordLengthLabel))
    passwordSliderLayout.add_widget(passwordLengthSlider)
    passwordLengthLayout.add_widget(passwordSliderLayout)
    mainLayout.add_widget(passwordLengthLayout)

    symbolLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
    symbolLayout.add_widget(
        Label(text='Include special symbol', font_size='15sp', size_hint_x=0.135)
    )
    symbolEnabledCheckBox = CheckBox(size_hint_x=0.2)
    symbolLayout.add_widget(symbolEnabledCheckBox)
    mainLayout.add_widget(symbolLayout)
    return {"Layout": mainLayout, "ApplicationName": applicationNameTextInput, "Username": usernameTextInput, "SymbolEnabledCheckBox": symbolEnabledCheckBox, "PasswordLength": passwordLengthSlider}

def onSliderValueChange(val,passwordLengthLabel):
    passwordLengthLabel.text = str(int(val))
