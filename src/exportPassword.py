from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard 
from kivymd.uix.filemanager import MDFileManager
from Database.LoginDetailsDB import LoginDetailsDB
from Database.EmailSettings import TwoFactorAuthenticationSettingsDB
from Util.UIUtil import *
from Util.two_factor_authentication import *
from cryptography.fernet import Fernet
import os

class ExportPassword:
    def __init__(self):
        self.encrypt_file_password = ""
        self.enable_encryption = False 
        self.two_factor_auth = TwoFactorAuthenticationSettingsDB()
        self.two_factor_auth_info = self.two_factor_auth.fetch_all_from_db()
        if self.two_factor_auth_info and self.two_factor_auth_info.enable_2FA:
            create_2FA_popup_layout(self.createEncryptFilePopUp)
        else:
            self.createEncryptFilePopUp()

    def createEncryptFilePopUp(self):
        main_layout = BoxLayout(
            orientation = 'vertical',
            padding=10,
            spacing=10
        )
        pop_up = Popup(title='File Encryption',
                       content=main_layout,
                       size_hint=(None,None),
                       size=(600,600))

        main_layout.add_widget(Label(text='Would you like to encrypt the file?', size_hint_y=None, height='50dp'))

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        yes_button = Button(text='Yes', size_hint_x=0.5)
        yes_button.bind(on_press=lambda instance: (self.encryptionFileButton(True,pop_up)))

        no_button = Button(text='No', size_hint_x=0.5)
        no_button.bind(on_press=lambda instance: (self.encryptionFileButton(False,pop_up)))

        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        
        main_layout.add_widget(button_layout)
        
        pop_up.open()

    def encryptionFileButton(self,enable_encryption,pop_up):
        self.enable_encryption = enable_encryption
        pop_up.dismiss()
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
            
    def write_password_to_file(self):
        user_login_details = self.login_details.fetch_all_from_db() 
        file = open(self.export_dir + "/password.txt","w")
        for credentials in user_login_details:
            url = credentials.update_url if credentials.update_url else ""
            software_type = credentials.software_type if credentials.software_type else ""
            file.write("Website: " + credentials.website_name + "  Username: " + credentials.username + "  Password: " + credentials.password.rstrip()  + "  URL: " + url.rstrip() + "  Software Type: " + software_type.rstrip() + "\n")
        file.close()
        #TODO: Give users the option to encrypt the password file
        if self.enable_encryption:
            self.encrypt_password_file()
    
    def encrypt_password_file(self):
        self.encrypt_file_password = Fernet.generate_key()
        fernet = Fernet(self.encrypt_file_password)
        with open(self.export_dir + "/password.txt","rb") as f:
            file = f.read()
        encrypted = fernet.encrypt(file)
        with open(self.export_dir + "/password.txt",'wb') as f:
            f.write(encrypted)

    def exit_manager(self, *args):
        if self.export_dir != "":
            self.write_password_to_file()
            message = f'All your password have been exported to \n{self.export_dir}'
            if self.enable_encryption:
                Clipboard.copy(self.encrypt_file_password.decode("utf-8"))
                message += f"\nYour password file has been encrypted!\nPassword:{self.encrypt_file_password}\nPassword has been stored in your clipboard"
            show_popup('Password Exported',Label(text=message),(None,None),(500,500))
        else:
            show_popup('Cancelled',Label(text="You did not select a directory"))
        self.file_manager.close()

    def select_path(self, path):
        self.export_dir = path
        self.exit_manager()
