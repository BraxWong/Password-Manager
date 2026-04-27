from kivymd.uix.filemanager import MDFileManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from Database.LoginDetailsDB import LoginDetailsDB
from Util.UIUtil import *
import re
import os

class ImportPassword:
    def __init__(self, security_module):
        self.login_details = LoginDetailsDB()
        self.security_module = security_module
        self.selected_file = False
        self.selected_path = ""
        path = os.path.expanduser("~")
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path,
        )
        self.file_manager.show(path)

    def exit_manager(self, *args):
        if self.selected_path != "":
            self.read_file()
            title = 'Updated' if self.selected_file else 'Error'
            content = "Your user details have been updated" 
            show_popup(title,Label(text=content),(None,None),(600,600))
            self.security_module.audit_action('IMPORT_PASSWORD', 'User has imported password to the system.',True)
        else:
            show_popup('Cancelled',Label(text="You did not select a file"),(None,None),(600,600))
            self.security_module.audit_action('IMPORT_PASSWORD', 'User did not select a file.',False)
        self.file_manager.close()

    def select_path(self,path):
        self.selected_path = path
        self.exit_manager()

    def read_file(self):
        f = open(self.selected_path,"r")
        line_list = f.readlines()
        for line in line_list:
            line = line.replace("Website: ", '')
            username_index = [match.start() for match in re.finditer("Username: ",line)] 
            if len(username_index) == 0:
                self.selected_file = False
                return
            website = line[0:username_index[0]-2]
            line = line.replace(website+"  ",'')
            
            line = line.replace("Username: ",'')
            password_index = [match.start() for match in re.finditer("Password: ",line)]
            if len(password_index) == 0:
                self.selected_file = False
                return
            username = line[0:password_index[0]-2]
            line = line.replace(username+"  ",'')

            line = line.replace("Password: ",'') 
            url_index = [match.start() for match in re.finditer("URL: ",line)]
            if len(url_index) == 0:
                self.selected_file = False
                return
            password = line[0:url_index[0]-1]
            line = line.replace(password + " ",'')

            line = line.replace("URL: ",'')
            software_type_index = [match.start() for match in re.finditer("Software Type: ",line)]
            url = line[0:software_type_index[0]-2] 
            line = line.replace(url + "  ",'')

            line = line.replace("Software Type: ",'')
            software_type = line if line else ""

            self.login_details.add_entry_to_db(website,username,password,url,software_type)
        self.selected_file = True
