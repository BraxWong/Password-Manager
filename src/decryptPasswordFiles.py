from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivymd.uix.filemanager import MDFileManager
from Database.LoginDetailsDB import LoginDetailsDB
from Database.EmailSettings import TwoFactorAuthenticationSettingsDB
from Util.UIUtil import *
from Util.two_factor_authentication import *
from cryptography.fernet import Fernet
import os

class DecryptPasswordFiles:
    def __init__(self):
        self.import_path = ""
        self.encrypt_file_password = ""
        self.enable_encryption = False 
        self.two_factor_auth = TwoFactorAuthenticationSettingsDB()
        self.two_factor_auth_info = self.two_factor_auth.fetch_all_from_db()
        if self.two_factor_auth_info and self.two_factor_auth_info.enable_2FA:
            create_2FA_popup_layout(self.run)
        else:
            self.run(True)

    def run(self, result):
        if result:
            self.login_details = LoginDetailsDB()
            self.export_dir = ""
            path = os.path.expanduser("~")
            self.file_manager = MDFileManager(
                exit_manager = self.exit_manager,
                select_path = self.select_path,
            )
            self.file_manager.show(path)
        else:
            show_popup('Error',Label(text="The 2FA code you provided is incorrect.Please try again"))


    def display_password_encryption_input(self):
        main_layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=10
        )
        pop_up = Popup(title='Password',
                content=main_layout,
                size_hint=(None, None),
                size=(600, 600))

        main_layout.add_widget(Label(text='Please provide the password to decrypt this file',
                                    size_hint_y=None, height='50dp'))

        center_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', padding=[0,0,0,0])
        
        self.decrypt_password = TextInput(text='', multiline=False, size_hint=(None, None),
                                        size=('360dp', '40dp'))  

        center_box.add_widget(Widget(size_hint_x=1))
        center_box.add_widget(self.decrypt_password)
        center_box.add_widget(Widget(size_hint_x=1))

        main_layout.add_widget(center_box)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        submit_button = Button(text='Submit', size_hint_x=0.5)
        submit_button.bind(on_press=lambda instance: self.decrypt_password_file(self.decrypt_password.text, pop_up))
        button_layout.add_widget(submit_button)

        main_layout.add_widget(button_layout)

        pop_up.open()

    def decrypt_password_file(self,password,pop_up):
        try:
            fernet = Fernet(password.encode("utf-8"))
        except:
            show_popup('Error',Label(text="Your password is incorrect. Please try again."),(None,None),(500,500))
            return
       
        with open(self.import_path, 'rb') as f:
            encrypted = f.read()
        
        decrypted = fernet.decrypt(encrypted)
        decrypted = decrypted.decode('utf-8')
        for word in decrypted.split():
            if word != 'Website:':
                show_popup('Error',Label(text="Your password is incorrect. Please try again."),(None,None),(500,500))
                return
            break
        file = open(self.import_path,"w")
        file.write(decrypted)
        show_popup('Password Decrypted',Label(text="Your password file has been decrypted."),(None,None),(500,500))
        pop_up.dismiss()
        self.file_manager.close()

    def exit_manager(self, *args):
        show_popup('Cancelled',Label(text="You did not select a file"))
        self.file_manager.close()

    def select_path(self, path):
        self.import_path = path
        self.display_password_encryption_input()
