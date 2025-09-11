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
        self.main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),  
            padding=0,
            spacing=50  
        )

        self.top_row_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',  
            padding=(10, 0)  
        )

        self.back_button = MDRaisedButton(text="Back", on_release=self.on_button_press)
        self.top_row_layout.add_widget(self.back_button)

        self.top_row_layout.add_widget(
            Label(
                text='Create a Password',
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
        self.application_name_layout.add_widget(
            Label(
                text='Name of application/website',
                font_size='15sp',
                size_hint_x=0.4
            )
        )
        self.application_name_text_input = TextInput(
            text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.application_name_layout.add_widget(self.application_name_text_input)
        self.main_layout.add_widget(self.application_name_layout)

                
        self.username_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        self.username_layout.add_widget(
             Label(text='Username', font_size='15sp', size_hint_x=0.4)
        )
        self.username_text_input = TextInput(
             text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        self.username_layout.add_widget(self.username_text_input)
        self.main_layout.add_widget(self.username_layout)

        self.password_length_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp', spacing='10dp')
        self.password_length_layout.add_widget(
            Label(text='Length of password', font_size='15sp', size_hint_x=0.4)
        )
        self.password_slider_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        self.password_length_label = Label(text='14', font_size='20sp', halign='center')
        self.password_slider_layout.add_widget(self.password_length_label)
        self.password_length_slider = Slider(
            min=1, max=64, value=14, value_track=True, value_track_color=[1, 0, 0, 1]
        )
        self.password_length_slider.bind(value=self.on_slider_value_change)
        self.password_slider_layout.add_widget(self.password_length_slider)
        self.password_length_layout.add_widget(self.password_slider_layout)
        self.main_layout.add_widget(self.password_length_layout)

        self.symbol_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        self.symbol_layout.add_widget(
            Label(text='Include special symbol', font_size='15sp', size_hint_x=0.135)
        )
        self.symbol_enabled_checkbox = CheckBox(size_hint_x=0.2)
        self.symbol_layout.add_widget(self.symbol_enabled_checkbox)
        self.main_layout.add_widget(self.symbol_layout)

        self.generate_password_button = Button(
            text='Generate a password', size_hint=(None, None), height='40dp', width='200dp', pos_hint={'center_x': 0.5}
        )
        self.generate_password_button.bind(on_press=self.update_login_details_to_db)
        self.main_layout.add_widget(self.generate_password_button)
       
        self.main_layout.add_widget(Widget(size_hint_y=1))
        
        self.add_widget(self.main_layout)

    def on_slider_value_change(self,widget,val):
        self.password_length_label.text=str(int(val))

    def on_button_press(self, instance_button: MDRaisedButton):
        self.manager.current = 'Menu Screen'

    def update_login_details_to_db(self,widget):
        if not self.check_login_details():
            password = Util.Util.generate_password(self.symbol_enabled_checkbox.active, int(self.password_length_label.text))
            self.db.addEntryToDB(self.application_name_text_input.text,self.username_text_input.text,password)
            popup = Popup(title='Password Generated',
                            content=Label(text=f'Website:{self.application_name_text_input.text}\nUsername:{self.username_text_input.text}\nPassword:{password}\nSaved in Database'),
                            size_hint=(None,None),
                            size=(400,400))
            popup.open()
            self.reset_input_widget_value()
            return password

    def check_login_details(self):
        missing_information = False
        error_message = "Please provide the following information:\n"
        if self.application_name_text_input.text == "":
            error_message += "Name of the Application\n"
            missing_information = True
        if self.username_text_input.text == "":
            error_message += "Your Username"
            missing_information = True
        if missing_information:
            popup = Popup(title='Error',
                        content=Label(text=error_message),
                        size_hint=(None,None),
                        size=(400,400))
            popup.open()
        return missing_information

    def reset_input_widget_value(self):
        self.application_name_text_input.text = ''
        self.username_text_input.text = ''
        self.password_length_label.text = '14'
        self.symbol_enabled_checkbox.active = False
        self.password_length_slider.value = 14