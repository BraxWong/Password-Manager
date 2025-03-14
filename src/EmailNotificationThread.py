from Database.EmailSettings import *
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

    def stop(self):
        self.running = False
