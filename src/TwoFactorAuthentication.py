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

class TwoFactorAuthentication(Screen):
    def __init__(self, **kwargs):
        super(TwoFactorAuthentication, self).__init__(**kwargs)
        self.two_factor_authentication_db = TwoFactorAuthenticationSettingsDB()
        self.floatLayout = FloatLayout()

        self.mainLayout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),  
            height=300,  
            spacing=20
        )

        self.topRowLayout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp'
        )

        self.backButton = MDRaisedButton(text="Back", on_release=self.on_button_press)
        self.topRowLayout.add_widget(self.backButton)

        self.topRowLayout.add_widget(
            Label(
                text='Enable Email Notification For Password Changes',
                font_size='20sp',
                halign='center',
                size_hint_x=0.8
            )
        )

        self.mainLayout.add_widget(self.topRowLayout)

        self.emailAddressLayout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )

        self.emailAddressLayout.add_widget(
            Label(
                text='Email Address',
                font_size='15sp',
                size_hint_x=0.4
            )
        )
        self.emailAddressTextInput = TextInput(
            text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.emailAddressLayout.add_widget(self.emailAddressTextInput)
        self.mainLayout.add_widget(self.emailAddressLayout)

        self.phoneLayout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )

        self.phoneLayout.add_widget(
            Label(
                text='Phone Number',
                font_size='15sp',
                size_hint_x=0.4
            )
        )


        self.phoneTextInput = TextInput(
            text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.phoneLayout.add_widget(self.phoneTextInput)
        self.mainLayout.add_widget(self.phoneLayout)

        self.enableEmailNotificationLayout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )

        self.enableEmailNotificationLayout.add_widget(
            Label(text='Enable 2FA?', font_size='15sp', size_hint_x=0.135)
        )
        self.enableEmailNotificationCheckbox = CheckBox(size_hint_x=0.2)
        self.enableEmailNotificationLayout.add_widget(self.enableEmailNotificationCheckbox)

        two_factor_auth_info = self.two_factor_authentication_db.fetchAllFromDB()
        if len(two_factor_auth_info) != 0:
            self.emailAddressTextInput.text = two_factor_auth_info[0][0]
            self.phoneTextInput.text = two_factor_auth_info[0][1] 
            self.enableEmailNotificationCheckbox.active = True if two_factor_auth_info[0][1] else False

        self.mainLayout.add_widget(self.enableEmailNotificationLayout)

        self.mainLayout.pos_hint = {'top': 1}  # Push to top of screen
        self.floatLayout.add_widget(self.mainLayout)

        self.saveEmailNotificationSettingsButton = Button(
            text='Save Settings',
            size_hint=(None, None),
            height='40dp',
            width='200dp',
            pos_hint={'center_x': 0.5, 'bottom':1}
        )
        self.saveEmailNotificationSettingsButton.bind(on_press=self.saveEmailNotificationSettings)
        self.floatLayout.add_widget(self.saveEmailNotificationSettingsButton)

        self.add_widget(self.floatLayout)

    def on_button_press(self, instance_button: MDRaisedButton):
        self.manager.current = 'Menu Screen'

    def saveEmailNotificationSettings(self, widget):
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if  len(self.emailAddressTextInput.text) != 0 and not EMAIL_REGEX.match(self.emailAddressTextInput.text):
            popUp = Popup(title='Error',
                        content=Label(text="Please provide a valid email address"),
                        size_hint=(None,None),
                        size=(600,600))
            popUp.open()
            return
        else:
            update_email_addr = True
        if len(self.phoneTextInput.text) != 0 and not self.phoneTextInput.text.isdigit():
            popUp = Popup(title='Error',
                        content=Label(text="Please provide a valid phone number"),
                        size_hint=(None,None),
                        size=(600,600))
            popUp.open()
            return
        else:
            update_phone_number = True

        if self.enableEmailNotificationCheckbox.active and (len(self.emailAddressTextInput.text) == 0 and len(self.phoneTextInput.text) == 0):
            popUp = Popup(title='Error',
                                content=Label(text="Please provide a valid phone number / email address"),
                                size_hint=(None,None),
                                size=(600,600))
            popUp.open()
            return
             
        self.two_factor_authentication_db.addEntryToDB(self.emailAddressTextInput.text, self.phoneTextInput.text, self.enableEmailNotificationCheckbox.active)
        popUp = Popup(title='Success',
                    content=Label(text="Your 2FA settings have been saved."),
                    size_hint=(None,None),
                    size=(600,600))
        popUp.open()
