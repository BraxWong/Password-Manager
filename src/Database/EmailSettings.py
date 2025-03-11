import sqlite3
import os
from datetime import datetime

class LoginDetailsDB:

    def __init__(self):
        self.PATHTOSQLDIR='Database/SQLFiles'
        if not os.path.isdir(self.PATHTOSQLDIR):
            os.makedirs(self.PATHTOSQLDIR)
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/EmailSettings.db')
        #Creates a cursor to the database
        self.cur=self.con.cursor()
        self.createLoginDetailsTable()

    def createLoginDetailsTable(self):
        self.cur.execute(
            "CREATE TABLE if not exists email_settings(email_address, enable_notifications, last_notification)"
        )

    def addEntryToDB(self,emailAddress, enableNotifications):
        if self.emailAddressSet(emailAddress):
            self.updateEmailSettings(emailAddress,True)
        else:
            self.cur.execute(
                f'INSERT INTO email_settings VALUES ("{emailAddress}","{enableNotifications}","{datetime.now().date()}")'
            )
            self.con.commit()

    def fetchAllFromDB(self):
        self.cur.execute(
            "SELECT * FROM email_settings"
        )
        return self.cur.fetchall()

    def updateEmailSettings(self, email_address, enable_notifications):
        emailSettings = self.fetchAllFromDB()
        self.cur.execute('UPDATE email_settings SET email_address = ?, enable_notifications = ? WHERE email_address = ?, enable_notifications = ?',
            (email_address,enable_notifications,emailSettings[0],emailSettings[1])
        )
        self.con.commit()

    def updateLastNotification(self, last_notification):
        emailSettings = self.fetchAllFromDB()
        self.cur.execute('UPDATE email_settings SET last_notification = ? WHERE last_notification = ?',
                (last_notification, emailSettings[2])
        )
        self.con.commit()

    def emailAddressSet(self, email_address):
        emailSettings = self.fetchAllFromDB()
        if len(emailSettings) == 1:
            return emailSettings[0] == email_address
        return False
