from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager
from Database.LoginDetailsDB import LoginDetailsDB
from Database.EmailSettings import TwoFactorAuthenticationSettingsDB
from Util.UIUtil import *
from Util.two_factor_authentication import *
import os

class ExportPassword:
    def __init__(self):
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
            show_incorrect_2FA_popup()
    def write_password_to_file(self):
        user_login_details = self.login_details.fetch_all_from_db()
        file = open(self.export_dir + "/password.txt","w")
        for credentials in user_login_details:
            url = credentials.update_url if credentials.update_url else ""
            file.write("Website: " + credentials.website_name + "  Username: " + credentials.username + "  Password: " + credentials.password.rstrip() + " URL: " + url + "\n")
        file.close()

    def exit_manager(self, *args):
        if self.export_dir != "":
            self.write_password_to_file()
            show_popup('Password Exported',Label(text=f'All your password have been exported to \n{self.export_dir}'))
        else:
            show_popup('Cancelled',Label(text="You did not select a directory"))
        self.file_manager.close()

    def select_path(self, path):
        self.export_dir = path
        self.exit_manager()
