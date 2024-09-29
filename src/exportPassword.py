from Database.LoginDetailsDB import LoginDetailsDB

class ExportPassword:
    def __init__(self,filePath):
        self.filePath = filePath
        self.loginDetails = LoginDetailsDB()
        self.writePasswordToFile()

    def writePasswordToFile(self):
        userLoginDetails = self.loginDetails.fetchAllFromDB()
        file = open("password.txt","w")
        for password in userLoginDetails:
            file.write(password[0] + "  " + password[1] + "\n")
        file.close()


