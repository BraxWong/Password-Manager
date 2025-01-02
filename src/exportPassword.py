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
            file.write("Website: " + password[0] + "  " + "Username: " + password[1] + "  " + "Password: " + password[2] + "\n")
        file.close()


