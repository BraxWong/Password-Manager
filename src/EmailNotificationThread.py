from Database.EmailSettings import *
from Database.LoginDetailsDB import *
import subprocess
from datetime import datetime

class EmailNotificationThread:
    def __init__(self):
        self.running = False

    def run(self):
        self.running = True
        email_settings_db = TwoFactorAuthenticationSettingsDB()
        email_settings = email_settings_db.fetch_all_from_db()
        if email_settings:
            db_date = datetime.strptime(email_settings.last_notification, "%Y-%m-%d")
            date_difference = datetime.today() - db_date
            if int(str(date_difference)[0]) >= 15 and email_settings.enable_2FA:
                email_header = "Password Manager Reminder"
                email_body = "Dear User,\nOne (or more) of your login details have not been changed in the past 15 days. Please generate a new password to ensure the security of your login details. Thanks, and have a wonderful day.\n\nKindest Regards,\nPassword Manager Team"
                subprocess.run(f'cd src/Util && ./EmailSender "{email_settings.email_address}" "{email_header}" "{email_body}"', 
                            shell=True, capture_output=True, text=True)
        self.stop()

    def sendLoginDetails(self):
        self.running = True 
        self.loginDetails = LoginDetailsDB()
        user_login_details = self.loginDetails.fetch_all_from_db()
        email_settings_db = TwoFactorAuthenticationSettingsDB()
        email_settings = email_settings_db.fetch_all_from_db()
        file = open("password.txt","w")
        user_credentials = ''
        for login_credential in user_login_details:
            user_credentials += "Website: " + login_credential[0] + "  Username: " + login_credential[1] + "  Password: " + login_credential[2].rstrip() + "\n"
        email_header = "Password Manager User Credentials Exportation"
        email_body = "Dear User,\nYour user credentials have been exported to your email address as requested. It has been attached along with this email. Please do not hesitate to reach out if you have any issues with this service. Thank you for choosing our service.\nKindest Regards,\nPassword Manager Team"
        subprocess.run(f'cd src/Util && ./EmailSender "{email_settings.email_address}" "{email_header}" "{email_body}" "{user_credentials}"', 
                            shell=True, capture_output=True, text=True)
        self.stop()
        
    def stop(self):
        self.running = False
