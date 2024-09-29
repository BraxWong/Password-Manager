from plyer import filechooser
from Database.LoginDetailsDB import LoginDetailsDB

class ExportPassword:
    def __init__(self):
        self.loginDetails = LoginDetailsDB()
        self.path = filechooser.choose_dir(title="Choose a directory to store your password",
                                           path="")[0] + "/password.txt"
        self.writePasswordToFile()

    def writePasswordToFile(self):
        userLoginDetails = self.loginDetails.fetchAllFromDB()
        file = open(self.path,"w")
        for password in userLoginDetails:
            file.write(password[0] + "  " + password[1] + "\n")
        file.close()


