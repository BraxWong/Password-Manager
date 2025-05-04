from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.filemanager import MDFileManager
from Database.LoginDetailsDB import LoginDetailsDB
import os

class ExportPassword:
    def __init__(self):
        self.loginDetails = LoginDetailsDB()
        self.exportDir = ""
        path = os.path.expanduser("~")
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path,
        )
        self.file_manager.show(path)

    def writePasswordToFile(self):
        userLoginDetails = self.loginDetails.fetchAllFromDB()
        file = open(self.exportDir + "/password.txt","w")
        for password in userLoginDetails:
            file.write("Website: " + password[0] + "  Username: " + password[1] + "  Password: " + password[2].rstrip() + "\n")
        file.close()

    def exit_manager(self, *args):
        if self.exportDir != "":
            self.writePasswordToFile()
            popup = Popup(title='Password Exported',
                          content=Label(text=f'All your password have been exported to \n{self.exportDir}'),
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
        self.exportDir = path
        self.exit_manager()
