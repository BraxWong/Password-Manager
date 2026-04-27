import sqlite3
from datetime import datetime
import Util.OSUtil

class UserAudit:
    def __init__(self, username, action, date, description, action_completion, machine_name, ip_address):
        self.username = username
        self.action = action
        self.date = date 
        self.description = description
        self.action_completion = action_completion
        self.machine_name = machine_name
        self.ip_address = ip_address

class UserAuditDB:
    def __init__(self):
        self.PATHTOSQLDIR=Util.OSUtil.getOSDBPath()
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/UserAudit.db')
        #Creates a cursor to the database
        self.cur=self.con.cursor()
        self.todays_date = datetime.now().date()
        self.create_user_audit_table()

    def create_user_audit_table(self):
        self.cur.execute(
            "CREATE TABLE if not exists user_audit(username, action, date, description, action_completion, machine_name, ip_address)"
        )

    def add_entry_to_db(self, username, action, date, description, action_completion, machine_name, ip_address):
        self.cur.execute(
            f'INSERT INTO user_audit VALUES ("{username}","{action}","{date}","{description}","{action_completion}","{machine_name}","{ip_address}")'
        )
        self.con.commit()

    def fetch_all_from_db(self):
        self.cur.execute(
            "SELECT * FROM user_audit"
        )
        audit = self.cur.fetchall()
        user_audit = [
            UserAudit(username, action, date, description, action_completion, machine_name, ip_address) 
            for username, action, date, description, action_completion, machine_name, ip_address in audit 
        ]
        return user_audit