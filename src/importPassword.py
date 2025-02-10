from plyer import filechooser
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from Database.LoginDetailsDB import LoginDetailsDB
import re

class ImportPassword:
    def __init__(self):
        self.loginDetails = LoginDetailsDB()
        self.selectedFile = False
        try:
            self.path = filechooser.open_file(title="Select your password file",
                                           path="")[0]
            self.readFile()
        except Exception as e:
            if not self.selectedFile:
                popUp = Popup(title='Cancelled',
                            content=Label(text="You did not select a file."),
                            size_hint=(None,None),
                            size=(600,600))
                popUp.open()


    def readFile(self):
        f = open(self.path,"r")
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
        popUp = Popup(title='Updated',
                      content=Label(text="Your user details have been updated."),
                      size_hint=(None,None),
                      size=(600,600))
        popUp.open()
