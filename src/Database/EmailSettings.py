import sqlite3
import os
from datetime import datetime

class EmailSettingsDB:

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
        if self.emailAddressSet():
            self.updateEmailSettings(emailAddress,enableNotifications)
        else:
            self.cur.execute(
                f'INSERT INTO email_settings VALUES ("{emailAddress}",{enableNotifications},"{datetime.now().date()}")'
            )
            self.con.commit()

    def fetchAllFromDB(self):
        self.cur.execute(
            "SELECT * FROM email_settings"
        )
        return self.cur.fetchall()

    def updateEmailSettings(self, email_address, enable_notifications):
        emailSettings = self.fetchAllFromDB()
        self.cur.execute('UPDATE email_settings SET email_address = ?, enable_notifications = ? WHERE email_address = ? AND enable_notifications = ?',
            (email_address,enable_notifications,emailSettings[0][0],emailSettings[0][1])
        )
        self.con.commit()

    def updateLastNotification(self, last_notification):
        emailSettings = self.fetchAllFromDB()
        self.cur.execute('UPDATE email_settings SET last_notification = ? WHERE last_notification = ?',
                (last_notification, emailSettings[0][2])
        )
        self.con.commit()

    def emailAddressSet(self):
        emailSettings = self.fetchAllFromDB()
        return len(emailSettings) == 1
