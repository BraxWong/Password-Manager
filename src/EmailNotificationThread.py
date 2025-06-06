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
                subprocess.run(f'cd src/Util && ./EmailSender "{emailSettings[0][0]}" "{emailHeader}" "{emailBody}"', 
                            shell=True, capture_output=True, text=True)
        self.stop()

    def sendLoginDetails(self):
        self.running = True 
        self.loginDetails = LoginDetailsDB()
        userLoginDetails = self.loginDetails.fetchAllFromDB()
        emailSettingsDB = EmailSettingsDB()
        emailSettings = emailSettingsDB.fetchAllFromDB()
        file = open("password.txt","w")
        userCredentials = ''
        for loginCredential in userLoginDetails:
            userCredentials += "Website: " + loginCredential[0] + "  Username: " + loginCredential[1] + "  Password: " + loginCredential[2].rstrip() + "\n"
        emailHeader = "Password Manager User Credentials Exportation"
        emailBody = "Dear User,\nYour user credentials have been exported to your email address as requested. It has been attached along with this email. Please do not hesitate to reach out if you have any issues with this service. Thank you for choosing our service.\nKindest Regards,\nPassword Manager Team"
        subprocess.run(f'cd src/Util && ./EmailSender "{emailSettings[0][0]}" "{emailHeader}" "{emailBody}" "{userCredentials}"', 
                            shell=True, capture_output=True, text=True)
        self.stop()
        
    def stop(self):
        self.running = False
