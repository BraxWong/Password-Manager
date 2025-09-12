from Util.Util import *
from datetime import datetime
import subprocess
ONE_MINUTE = 60
CODE_LENGTH = 6

class twoFactorAuth:
    
    def __init__(self, contact_info):
        self.code = ""
        self.generate_timestamp = ""
        self.contact_info = contact_info
        self.generate_2FA_code()
        self.send_2FA_code_by_email()

    def generate_2FA_code(self):
        self.code = generate_password(True, CODE_LENGTH)
        self.generate_timestamp = datetime.now() 

    def send_2FA_code_by_email(self):
        email_header = "Password Manager 2FA Code"
        email_body = (f"Dear User,\n\nYour 2FA code is {self.code}. "
                      "Please note that the code will only be valid for 1 minute. "
                      "If you did not request this action, that means your system has been compromised. "
                      "Thanks and have a great day.\n\nKindest Regards,\nPassword Manager Team")
        
        result = subprocess.run(
            f'cd src/Util && ./EmailSender "{self.contact_info}" "{email_header}" "{email_body}"', 
            shell=True, capture_output=True, text=True
        )

        if result.returncode != 0:
            print("Error sending email:", result.stderr)

    def auth_expired(self):
        time_difference = datetime.now() - self.generate_timestamp
        return time_difference.seconds >= ONE_MINUTE 

