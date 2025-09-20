from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton
from Database.LoginDetailsDB import LoginDetailsDB  
import requests
import hashlib

class LoginDetailsStorage(Screen):

    def __init__(self, **kwargs):
        super(LoginDetailsStorage,self).__init__(**kwargs)

        self.db = LoginDetailsDB()
        self.main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),  
            padding=0,
            spacing=50  
        )
        self.top_row_layout = BoxLayout(orientation='horizontal', 
                                      size_hint_y=None, 
                                      height=50, 
                                      padding=(10, 0))
        self.back_button = MDRaisedButton(text="Back", on_release=self.on_button_press)
        self.top_row_layout.add_widget(self.back_button)
        self.top_row_layout.add_widget(Label(text='Store Login Details', 
                                           font_size='20sp', 
                                           halign='center',
                                           size_hint_x=0.8
                                           )
                                    )
        self.main_layout.add_widget(self.top_row_layout)

        self.application_name_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height='50dp',
                spacing='10dp'
            )
        self.application_name_layout.add_widget(Label(text='Name of Application/Website',
                                                    font_size='15sp',
                                                    size_hint_x=0.4)
                                            )
        self.application_name_text_input = TextInput(text='', 
                                                  multiline=False,
                                                  size_hint=(0.6,None), 
                                                  height='40dp')
        self.application_name_layout.add_widget(self.application_name_text_input)
        self.main_layout.add_widget(self.application_name_layout)

        self.update_url_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height='50dp',
                spacing='10dp'
            )

        self.update_url_layout.add_widget(Label(text='Update Password URL',
                                          font_size='15sp',
                                          size_hint_x=0.4))
        self.update_url_text_input = TextInput(text='',
                                               multiline=False,
                                               size_hint=(0.6,None),
                                               height='40dp')
        self.update_url_layout.add_widget(self.update_url_text_input)
        self.main_layout.add_widget(self.update_url_layout)

        self.username_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        self.username_layout.add_widget(
             Label(text='Username', font_size='15sp', size_hint_x=0.4)
        )
        self.username_text_input = TextInput(
             text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.username_layout.add_widget(self.username_text_input)
        self.main_layout.add_widget(self.username_layout)

        self.password_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        self.password_layout.add_widget(
             Label(text='Password', font_size='15sp', size_hint_x=0.4)
        )
        self.password_text_input = TextInput(
             text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.password_layout.add_widget(self.password_text_input)
        self.main_layout.add_widget(self.password_layout)

        self.check_password_pwned_layout = BoxLayout(orientation='horizontal',size_hint_y=None, height='50dp', spacing='10dp')
        self.check_password_pwned_layout.add_widget(
             Label(text='Check Password Leakage', font_size='15sp',size_hint_x=0.4)
        )
        self.check_password_button = Button(text='Confirm',
                                          size_hint=(0.6, None), 
                                          height='40dp')

        self.check_password_button.bind(on_press=self.check_password_pwned)
        self.check_password_pwned_layout.add_widget(self.check_password_button)

        self.main_layout.add_widget(self.check_password_pwned_layout)

        self.store_login_details_button = Button(text='Store Login Details',
                                             size_hint=(None,None),
                                             height='40dp',
                                             width='200dp',
                                             pos_hint={'center_x':0.5})
        self.store_login_details_button.bind(on_press=self.store_login_details)
        self.main_layout.add_widget(self.store_login_details_button)
        self.main_layout.add_widget(Widget(size_hint_y=1))
        self.add_widget(self.main_layout)
       
    def on_button_press(self, instance_button: MDRaisedButton):
        self.manager.current = 'Menu Screen'

    def check_password_pwned(self,widget,show_popup=True):
        password_pwned = False
        if len(self.password_text_input.text) > 0:
            password_hash = hashlib.sha1(self.password_text_input.text.encode()).hexdigest().upper()
            pass_sha = password_hash[:5]
            apiKey = f'https://api.pwnedpasswords.com/range/{pass_sha}' 
            r = requests.get(apiKey)
            hashes = (line.split(":") for line in r.text.splitlines())
            for h, count in hashes:
                if h == password_hash[5:]:
                    password_pwned = True
                    pop_up = Popup(title="WARNING",
                                  content=Label(text=f"WARNING!!!\nYOUR PASSWORD HAS BEEN FOUND {count} TIMES!!!\nCHANGE YOUR PASSWORD NOW!!!!"),
                                  size_hint=(None,None),
                                  size=(600,600))
                    pop_up.open()
            if not password_pwned and show_popup:
                popup = Popup(title="Safe",
                            content=Label(text="Your password is safe."),
                            size_hint=(None,None),
                            size=(600,600))
                popup.open()
        else:
            password_pwned = True
            popup = Popup(title="Error",
                          content=Label(text="Please provide a password before checking for leaks."),
                          size_hint=(None,None),
                          size=(600,600))
            popup.open()
        return password_pwned

    def store_login_details(self,widget): 
        if len(self.application_name_text_input.text) > 0 and len(self.username_text_input.text) > 0 and len(self.password_text_input.text) > 0:
            if not self.check_password_pwned(None,False):
                self.db.add_entry_to_db(self.application_name_text_input.text,self.username_text_input.text,self.password_text_input.text,self.update_url_text_input.text) 
                popup = Popup(title='Password Stored',
                                        content=Label(text=f'Website:{self.application_name_text_input.text}\nUsername:{self.username_text_input.text}\nPassword:{self.password_text_input.text}\nSaved in Database'),
                                        size_hint=(None,None),
                                        size=(400,400))
                popup.open()
                self.application_name_text_input.text = ""
                self.update_url_text_input.text = ""
                self.username_text_input.text = ""
                self.password_text_input.text = ""
        else:
            error_message = "The following information is missing:"
            if len(self.application_name_text_input.text) <= 0:
                error_message += "\nApplication Name"
            if len(self.username_text_input.text) <= 0:
                error_message += "\nUsername"
            if len(self.password_text_input.text) <= 0:
                error_message += "\nPassword"
            popUp = Popup(title='Error',
                            content=Label(text=error_message),
                            size_hint=(None,None),
                            size=(400,400))
            popUp.open()

