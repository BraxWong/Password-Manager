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

def create_2FA_popup_layout(callback):
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

    pop_up = Popup(title='2FA',
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
        check_2FA_code(two_factor_auth_text_input.text, auth_system, pop_up, callback)

    submit_button = MDRaisedButton(
        text="Submit",
        size_hint=(None, None),  
        size=(200, 50),          
        on_release=on_submit,
        pos_hint={'center_x': 0.5}
    )
    main_layout.add_widget(submit_button)
    pop_up.open()

def show_incorrect_2FA_popup():
    pop_up = Popup(title='Error',
                  content=Label(text="The 2FA code you provided is incorrect.Please try again."),
                  size_hint=(None,None),
                  size=(400,400))
    pop_up.open() 

def createLoginDetailPopupLayout():
    main_layout = BoxLayout(
                orientation='vertical',
                size_hint=(1, 1),  
                padding=0,
                spacing=50 
            )
    application_name_layout = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height='50dp',
        spacing='10dp'
    )
    application_name_layout.add_widget(
        Label(
            text='Name of application/website',
            font_size='15sp',
            size_hint_x=0.4
        )
    )
    application_name_text_input = TextInput(
        text='', multiline=False, size_hint=(0.6, None), height='40dp'
    )
    application_name_layout.add_widget(application_name_text_input)
    main_layout.add_widget(application_name_layout)

            
    username_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
    username_layout.add_widget(
        Label(text='Username', font_size='15sp', size_hint_x=0.4)
    )
    username_text_input = TextInput(
        text='', multiline=False, size_hint=(0.6, None), height='40dp'
    )
    username_layout.add_widget(username_text_input)
    main_layout.add_widget(username_layout)

    password_length_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp', spacing='10dp')
    password_length_layout.add_widget(
        Label(text='Length of password', font_size='15sp', size_hint_x=0.4)
    )
    password_slider_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
    password_length_label = Label(text='14', font_size='20sp', halign='center')
    password_slider_layout.add_widget(password_length_label)
    password_length_slider = Slider(
        min=1, max=64, value=14, value_track=True, value_track_color=[1, 0, 0, 1]
    )
    password_length_slider.bind(value=lambda instance, value:on_slider_value_change(value,password_length_label))
    password_slider_layout.add_widget(password_length_slider)
    password_length_layout.add_widget(password_slider_layout)
    main_layout.add_widget(password_length_layout)

    symbol_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
    symbol_layout.add_widget(
        Label(text='Include special symbol', font_size='15sp', size_hint_x=0.135)
    )
    symbol_enabled_check_box = CheckBox(size_hint_x=0.2)
    symbol_layout.add_widget(symbol_enabled_check_box)
    main_layout.add_widget(symbol_layout)
    return {"Layout": main_layout, "ApplicationName": application_name_text_input, "Username": username_text_input, "SymbolEnabledCheckBox": symbol_enabled_check_box, "PasswordLength": password_length_slider}

def on_slider_value_change(val,password_length_label):
    password_length_label.text = str(int(val))
