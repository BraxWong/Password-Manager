import sqlite3
import Util.Util

class VerifyUser:
    def __init__(self, password, hint):
        self.password = password
        self.hint = hint

class VerifyUserDB:
    def __init__(self):
        self.PATHTOSQLDIR=Util.OSUtil.getOSDBPath()
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/VerifyUser.db')
        self.cur=self.con.cursor()
        self.create_verify_user_table()

    def create_verify_user_table(self):
        self.cur.execute(
            "CREATE TABLE if not exists verify_user(password,hint)"
        )
    
    def get_user_password_and_hint(self):
        self.cur.execute(
            "SELECT * FROM verify_user"
        )
        info = self.cur.fetchall()
        verify_user = VerifyUser(info[0][0], info[0][1])
        return verify_user
    
    def add_password_and_hint(self, password, hint):
        self.cur.execute(
            f'INSERT INTO verify_user VALUES("{password}", "{hint}")'
        )
        self.con.commit()

    def remove_password_and_hint(self):
        self.cur.execute(
            f'DELETE * FROM verify_user'
        )
        self.con.commit()
