from plyer import filechooser
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from Database.LoginDetailsDB import LoginDetailsDB

class ExportPassword:
    def __init__(self):
        self.loginDetails = LoginDetailsDB()
        self.selectedDir = False
        try:
            self.path = filechooser.choose_dir(title="Choose a directory to store your password",
                                            path="")[0] + "/password.txt"
            self.writePasswordToFile()
            popup = Popup(title='Password Exported',
                      content=Label(text=f'All your password have been exported to \n{self.path}'),
                      size_hint=(None,None),
                      size=(400,400))
            popup.open()
            return
        except Exception as e:
            if not self.selectedDir:
                popUp = Popup(title='Cancelled',
                            content=Label(text="You did not select a directory."),
                            size_hint=(None,None),
                            size=(600,600))
                popUp.open()


    def writePasswordToFile(self):
        userLoginDetails = self.loginDetails.fetchAllFromDB()
        file = open(self.path,"w")
        for password in userLoginDetails:
            file.write("Website: " + password[0] + "  Username: " + password[1] + "  Password: " + password[2].rstrip() + "\n")
        file.close()
        self.selectedDir = True
