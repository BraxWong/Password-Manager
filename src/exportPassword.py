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
        self.two_factor_auth_info = self.two_factor_auth.fetchAllFromDB()
        if not len(self.two_factor_auth_info) or not self.two_factor_auth_info[0][1]:
            self.run(True)
        else:
            create_2FA_popup_layout(self.run)

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
        user_login_details = self.login_details.fetchAllFromDB()
        file = open(self.export_dir + "/password.txt","w")
        for password in user_login_details:
            file.write("Website: " + password[0] + "  Username: " + password[1] + "  Password: " + password[2].rstrip() + "\n")
        file.close()

    def exit_manager(self, *args):
        if self.export_dir != "":
            self.write_password_to_file()
            popup = Popup(title='Password Exported',
                          content=Label(text=f'All your password have been exported to \n{self.export_dir}'),
                          size_hint=(None,None),
                          size=(400,400))
            popup.open()
        else:
            popUp = Popup(title='Cancelled',
                          content=Label(text="You did not select a directory."),
                          size_hint=(None,None),
                          size=(600,600))
            popUp.open()
        self.file_manager.close()

    def select_path(self, path):
        self.export_dir = path
        self.exit_manager()
