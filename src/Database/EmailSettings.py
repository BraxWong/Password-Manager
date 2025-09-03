import sqlite3
from datetime import datetime
import Util.OSUtil

class TwoFactorAuthenticationSettingsDB:

    def __init__(self):
        self.PATHTOSQLDIR=Util.OSUtil.getOSDBPath()
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/TwoFASettings.db')
        #Creates a cursor to the database
        self.cur=self.con.cursor()
        self.createLoginDetailsTable()

    def createLoginDetailsTable(self):
        self.cur.execute(
            "CREATE TABLE if not exists two_factor_auth_settings(email_address, phone_number, enable_notifications, last_notification)"
        )

    def addEntryToDB(self,email_address, phone_number, enable_notifications):
        two_factor_auth = self.fetchAllFromDB()
        if len(two_factor_auth):
            self.updateInfo(email_address, phone_number, enable_notifications)
        else:
            self.cur.execute(
                f'INSERT INTO two_factor_auth_settings VALUES ("{email_address}", "{phone_number}", {enable_notifications},"{datetime.now().date()}")'
            )
            self.con.commit()

    def fetchAllFromDB(self):
        self.cur.execute(
            "SELECT * FROM two_factor_auth_settings"
        )
        return self.cur.fetchall()

    def updateInfo(self, email_address, phone_number, enable_notifications):
        two_factor_auth = self.fetchAllFromDB()
        self.cur.execute('UPDATE two_factor_auth_settings SET email_address = ?, phone_number = ?, enable_notifications = ? WHERE email_address = ?',
            (email_address, phone_number, enable_notifications, two_factor_auth[0][0])
        )
        self.con.commit()

    def updateLastNotification(self, last_notification):
        two_factor_auth = self.fetchAllFromDB()
        self.cur.execute('UPDATE two_factor_auth_settings SET last_notification = ? WHERE last_notification = ?',
                (last_notification,two_factor_auth[0][3])
        )
        self.con.commit()
