from plyer import filechooser
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from Database.LoginDetailsDB import LoginDetailsDB

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
            #FIXME: The following parsing method does not work if the website, username, or the password involves spaces.
            line = line.replace("Website: ", '')
            line = line.replace("Username: ",'')
            line = line.replace("Password: ",'')
            line = line.strip()
            loginDetails = line.split()
            self.loginDetails.addEntryToDB(loginDetails[0],loginDetails[1],loginDetails[2])
        self.selectedFile = True
        popUp = Popup(title='Updated',
                      content=Label(text="Your user details have been updated."),
                      size_hint=(None,None),
                      size=(600,600))
        popUp.open()
