import sqlite3
import os

class LoginDetailsDB:
    def __init__(self):
        self.PATHTOSQLDIR='Database/SQLFiles'
        if not os.path.isdir(self.PATHTOSQLDIR):
            os.makedirs(self.PATHTOSQLDIR)
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/LoginDetails.db')
        #Creates a cursor to the database
        self.cur=self.con.cursor()
        self.createLoginDetailsTable()

    def createLoginDetailsTable(self):
        self.cur.execute(
            "CREATE TABLE if not exists login_details(website_name, password)"
        )

    def addEntryToDB(self,websiteName,password):
        if self.websitePasswordSet(websiteName):
            self.updateEntryToDB(websiteName,password)
        else:
            self.cur.execute(
                f'INSERT INTO login_details VALUES ("{websiteName}", "{password}")'
            )
            self.con.commit()

    def updateEntryToDB(self,websiteName,password):
        self.cur.execute(
            f'UPDATE login_details SET password = \'{password}\' WHERE website_name = \'{websiteName}\''
        )
        self.con.commit()
    
    #WARNING: The following function is only used for testing purposes for now. DO NOT USE
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

