import sqlite3
import os
from datetime import datetime

class LoginDetailsDB:
    def __init__(self):
        self.PATHTOSQLDIR='Database/SQLFiles'
        if not os.path.isdir(self.PATHTOSQLDIR):
            os.makedirs(self.PATHTOSQLDIR)
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/LoginDetails.db')
        #Creates a cursor to the database
        self.cur=self.con.cursor()
        self.todays_date = datetime.now().date()
        self.createLoginDetailsTable()

    def createLoginDetailsTable(self):
        self.cur.execute(
            "CREATE TABLE if not exists login_details(website_name, username, password, date_created)"
        )

    def addEntryToDB(self,websiteName,username,password):
        if self.websitePasswordSet(websiteName):
            self.updateEntryToDB(websiteName,username,password)
        else:
            self.cur.execute(
                f'INSERT INTO login_details VALUES ("{websiteName}","{username}","{password}","{self.todays_date}")'
            )
            self.con.commit()

    def updateEntryToDB(self,websiteName,username,password):
        self.cur.execute('UPDATE login_details SET password = ?, username = ?, date_created = ? WHERE website_name = ?',
            (password, username, self.todays_date, websiteName)
        )
        self.con.commit()
    
    def removeEntryFromDB(self,websiteName):
        self.cur.execute(
            f'DELETE FROM login_details WHERE website_name = \'{websiteName}\''
        )
        self.con.commit()

    def fetchAllFromDB(self):
        self.cur.execute(
            "SELECT * FROM login_details"
        )
        return self.cur.fetchall()

    def fetchWebsitePassword(self,websiteName):
        self.cur.execute(
            f'SELECT password FROM login_details WHERE website_name = \'{websiteName}\''
        )
        return self.cur.fetchone()

    def websitePasswordSet(self,websiteName):
        passwordSet=False
        self.cur.execute(
            f'SELECT * FROM login_details WHERE website_name=\'{websiteName}\''
        )
        if len(self.cur.fetchall()) >= 1:
            passwordSet=True
        return passwordSet

