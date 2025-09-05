from Util.Util import *
from datetime import datetime
import subprocess
ONE_MINUTE = 60

class twoFactorAuth:
    
    def __init__(self, send_by_email, contact_info):
        self.code = ""
        self.generate_timestamp = ""
        self.send_by_email = send_by_email
        self.contact_info = contact_info
        self.generate_2FA_code()
        if self.send_by_email:
            self.send_2FA_code_by_email()
        else:
            self.send_2FA_code_by_SMS()

    def generate_2FA_code(self):
        self.code = generatePassword(True, 6)
        self.generate_timestamp = datetime.now() 

    def send_2FA_code_by_email(self):
        email_header = "Password Manager 2FA Code"
        email_body = f"Dear User,\nYour 2FA is {self.code}. Please note that the code will only be valid for 1 minute. If you did not request this action, that means your system has been compromised. Thanks and have a great day.\n\nKindest Regards,\nPassword Manager Team"
        subprocess.run(f'cd src/Util && ./EmailSender "{self.contact_info}" "{email_header}" "{email_body}"', 
                            shell=True, capture_output=True, text=True)

    def send_2FA_code_by_SMS(self):
#                 ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
#                 ┃                                             ┃
#                 ┃ TODO: Figure out how to send SMS via python ┃
#                 ┃                                             ┃
#                 ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
        pass

    def auth_expired(self):
        time_difference = datetime.now() - self.generate_timestamp
        return time_difference.seconds >= ONE_MINUTE 
