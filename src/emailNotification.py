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
from Database.LoginDetailsDB import *
from Database.VerifyUserDB import *

class EmailNotification(Screen):
    def __init__(self, **kwargs):
        super(EmailNotification, self).__init__(**kwargs)

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

        self.enableEmailNotificationLayout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )

        self.enableEmailNotificationLayout.add_widget(
            Label(text='Enable Email Notification?', font_size='15sp', size_hint_x=0.135)
        )
        self.enableEmailNotificationCheckbox = CheckBox(size_hint_x=0.2)
        self.enableEmailNotificationLayout.add_widget(self.enableEmailNotificationCheckbox)
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
        pass