import sqlite3
from datetime import datetime
import Util.OSUtil

class TwoFactorAuthenticationSettings:
    def __init__(self, email_address, enable_2FA, last_notification):
        self.email_address = email_address
        self.enable_2FA = enable_2FA
        self.last_notification = last_notification

class TwoFactorAuthenticationSettingsDB:

    def __init__(self):
        self.PATHTOSQLDIR=Util.OSUtil.getOSDBPath()
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/TwoFASettings.db')
        #Creates a cursor to the database
        self.cur=self.con.cursor()
        self.create_two_factor_table()

    def create_two_factor_table(self):
        self.cur.execute(
            "CREATE TABLE if not exists two_factor_auth_settings(email_address, enable_notifications, last_notification)"
        )

    def add_entry_to_db(self,email_address, enable_notifications):
        two_factor_auth = self.fetch_all_from_db()
        if two_factor_auth:
            self.update_info(email_address, enable_notifications)
        else:
            self.cur.execute(
                f'INSERT INTO two_factor_auth_settings VALUES ("{email_address}", {enable_notifications},"{datetime.now().date()}")'
            )
            self.con.commit()

    def fetch_all_from_db(self):
        self.cur.execute(
            "SELECT * FROM two_factor_auth_settings"
        )
        info = self.cur.fetchall()
        if len(info) > 0:
            two_factor_settings = TwoFactorAuthenticationSettings(info[0][0],info[0][1],info[0][2])
            return two_factor_settings
        else:
            return 0

    def update_info(self, email_address, enable_notifications):
        two_factor_auth = self.fetch_all_from_db()
        self.cur.execute('UPDATE two_factor_auth_settings SET email_address = ?, enable_notifications = ? WHERE email_address = ?',
            (email_address, enable_notifications, two_factor_auth.email_address)
        )
        self.con.commit()

    def update_last_notification(self, last_notification):
        two_factor_auth = self.fetch_all_from_db()
        self.cur.execute('UPDATE two_factor_auth_settings SET last_notification = ? WHERE last_notification = ?',
                (last_notification,two_factor_auth.last_notification)
        )
        self.con.commit()
