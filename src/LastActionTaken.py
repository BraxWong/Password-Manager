from datetime import datetime

FIFTEEN_MINUTES = 15 * 60

class LastActionTaken:
    def __init__(self):
        self.last_action = datetime.now()
    
    def update_time(self):
        self.last_action = datetime.now()

    def check_login_required(self):
        time_differece = datetime.now() - self.last_action
        return time_differece.seconds >= FIFTEEN_MINUTES  