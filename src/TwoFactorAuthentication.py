from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from Database.EmailSettings import *
import re
import Util.UIUtil as UIUtil

class TwoFactorAuthentication(Screen):
    def __init__(self, **kwargs):
        super(TwoFactorAuthentication, self).__init__(**kwargs)
        self.two_factor_authentication_db = TwoFactorAuthenticationSettingsDB()
        self.float_layout = FloatLayout()

        self.main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),  
            height=300,  
            spacing=20
        )

        self.top_row_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp'
        )

        self.back_button = MDRaisedButton(text="Back", on_release=self.on_button_press)
        self.top_row_layout.add_widget(self.back_button)

        self.top_row_layout.add_widget(
            Label(
                text='Enable Email Notification For Password Changes',
                font_size='20sp',
                halign='center',
                size_hint_x=0.8
            )
        )

        self.main_layout.add_widget(self.top_row_layout)

        self.email_address_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )

        self.email_address_layout.add_widget(
            Label(
                text='Email Address',
                font_size='15sp',
                size_hint_x=0.4
            )
        )
        self.email_address_text_input = TextInput(
            text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.email_address_layout.add_widget(self.email_address_text_input)
        self.main_layout.add_widget(self.email_address_layout)

        self.enable_email_notification_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )

        self.enable_email_notification_layout.add_widget(
            Label(text='Enable 2FA?', font_size='15sp', size_hint_x=0.135)
        )
        self.enable_email_notification_checkbox = CheckBox(size_hint_x=0.2)
        self.enable_email_notification_layout.add_widget(self.enable_email_notification_checkbox)

        two_factor_auth_info = self.two_factor_authentication_db.fetch_all_from_db()
        if two_factor_auth_info:
            self.email_address_text_input.text = two_factor_auth_info.email_address
            self.enable_email_notification_checkbox.active = two_factor_auth_info.enable_2FA 

        self.main_layout.add_widget(self.enable_email_notification_layout)

        self.main_layout.pos_hint = {'top': 1} 
        self.float_layout.add_widget(self.main_layout)

        self.save_email_notification_settings_button = Button(
            text='Save Settings',
            size_hint=(None, None),
            height='40dp',
            width='200dp',
            pos_hint={'center_x': 0.5, 'bottom':1}
        )
        self.save_email_notification_settings_button.bind(on_press=self.saveEmailNotificationSettings)
        self.float_layout.add_widget(self.save_email_notification_settings_button)

        self.add_widget(self.float_layout)

    def on_button_press(self, instance_button: MDRaisedButton):
        self.manager.current = 'Menu Screen'

    def saveEmailNotificationSettings(self, widget):
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if len(self.email_address_text_input.text) != 0 and not EMAIL_REGEX.match(self.email_address_text_input.text):
            UIUtil.show_popup('Error',Label(text="Please provide a valid email address"))
            return
        else:
            update_email_addr = True

        if self.enable_email_notification_checkbox.active and len(self.email_address_text_input.text) == 0:
            UIUtil.show_popup('Error',Label(text="Please provide a valid email address"))
            return
             
        self.two_factor_authentication_db.add_entry_to_db(self.email_address_text_input.text, self.enable_email_notification_checkbox.active)
        UIUtil.show_popup('Success',Label(text="Your 2FA settings have been saved"))
