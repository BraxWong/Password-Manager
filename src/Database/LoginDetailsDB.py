import sqlite3
import os

class LoginDetailsDB:
    def __init__(self):
        self.PATHTOSQLDIR='Database/SQLFiles'
        if not os.path.isdir(self.PATHTOSQLDIR):
            os.makedirs(self.PATHTOSQLDIR)
        con=sqlite3.connect(self.PATHTOSQLDIR+'/LoginDetails.db')
        #Creates a cursor to the database
        self.cur=con.cursor()
        self.createLoginDetailsTable()

    def createLoginDetailsTable(self):
        self.cur.execute(
            "CREATE TABLE if not exists login_details(website_name, password)"
        )

    def addEntryToDB(self,websiteName,password):
        self.cur.execute(
            f'INSERT INTO login_details VALUES ("{websiteName}", "{password}")'
        )

    def fetchAllFromDB(self):
        self.cur.execute(
            "SELECT * FROM login_details"
        )
        print(self.cur.fetchall())

