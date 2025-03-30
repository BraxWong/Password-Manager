from Database.EmailSettings import *
from Database.LoginDetailsDB import *
import subprocess
from datetime import datetime

class EmailNotificationThread:
    def __init__(self):
        self.running = False

    def run(self):
        self.running = True
        emailSettingsDB = EmailSettingsDB()
        emailSettings = emailSettingsDB.fetchAllFromDB()
        if len(emailSettings) != 0:
            dbDate = datetime.strptime(emailSettings[0][2], "%Y-%m-%d")
            dateDifference = datetime.today() - dbDate
            if int(str(dateDifference)[0]) >= 15 and emailSettings[0][1]:
                emailHeader = "Password Manager Reminder"
                emailBody = "Dear User,\nOne (or more) of your login details have not been changed in the past 15 days. Please generate a new password to ensure the security of your login details. Thanks, and have a wonderful day.\n\nKindest Regards,\nPassword Manager Team"
                subprocess.run(f'cd Util && ./EmailSender "{emailSettings[0][0]}" "{emailHeader}" "{emailBody}"', 
                            shell=True, capture_output=True, text=True)
        self.stop()

    def sendLoginDetails(self):
        self.running = True 
        self.loginDetails = LoginDetailsDB()
        userLoginDetails = self.loginDetails.fetchAllFromDB()
        emailSettingsDB = EmailSettingsDB()
        emailSettings = emailSettingsDB.fetchAllFromDB()
        title = "Password Manager Login Detail Exports"
        emailBody = "Your details have been attached to this email down below."
        file = open("password.txt","w")
        for loginCredential in userLoginDetails:
            file.write("Website: " + loginCredential[0] + "  Username: " + loginCredential[1] + "  Password: " + loginCredential[2].rstrip() + "\n")
        file.close()
        # os.remove("password.txt")
        self.stop()
        
    def stop(self):
        self.running = False
