import sqlite3
import Util.Util

class VerifyUserDB:
    def __init__(self):
        self.PATHTOSQLDIR=Util.OSUtil.getOSDBPath()
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/VerifyUser.db')
        self.cur=self.con.cursor()
        self.createVerifyUserTable()

    def createVerifyUserTable(self):
        self.cur.execute(
            "CREATE TABLE if not exists verify_user(password,hint)"
        )
    
    def getUserPasswordAndHint(self):
        self.cur.execute(
            "SELECT * FROM verify_user"
        )
        return self.cur.fetchall()
    
    def addPasswordAndHint(self, password, hint):
        self.cur.execute(
            f'INSERT INTO verify_user VALUES("{password}", "{hint}")'
        )
        self.con.commit()

    def removePasswordAndHint(self):
        self.cur.execute(
            f'DELETE * FROM verify_user'
        )
        self.con.commit()
