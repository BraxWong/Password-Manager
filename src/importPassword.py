from kivymd.uix.filemanager import MDFileManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from Database.LoginDetailsDB import LoginDetailsDB
import re
import os

class ImportPassword:
    def __init__(self):
        self.loginDetails = LoginDetailsDB()
        self.selectedFile = False
        self.selectedPath = ""
        path = os.path.expanduser("~")
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path,
        )
        self.file_manager.show(path)

    def exit_manager(self, *args):
        if self.selectedPath != "":
            self.readFile()
            popUp = Popup(title='Updated',
                        content=Label(text="Your user details have been updated."),
                        size_hint=(None,None),
                        size=(600,600))
            popUp.open()        
        else:
            popUp = Popup(title='Cancelled',
                        content=Label(text="You did not select a file."),
                        size_hint=(None,None),
                        size=(600,600))
            popUp.open()
        self.file_manager.close()

    def select_path(self,path):
        self.selectedPath = path
        self.exit_manager()

    def readFile(self):
        f = open(self.selectedPath,"r")
        lineList = f.readlines()
        for line in lineList:
            line = line.replace("Website: ", '')
            usernameIndex = [match.start() for match in re.finditer("Username: ",line)] 
            website = line[0:usernameIndex[0]-2]
            line = line.replace(website+"  ",'')
            line = line.replace("Username: ",'')
            passwordIndex = [match.start() for match in re.finditer("Password: ",line)]
            username = line[0:passwordIndex[0]-2]
            line = line.replace(username+"  ",'')
            line = line.replace("Password: ",'')
            password = line
            self.loginDetails.addEntryToDB(website,username,password)
        self.selectedFile = True
 
