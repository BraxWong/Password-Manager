import sqlite3
from datetime import datetime
import Util.OSUtil

class LoginDetailsDB:
    def __init__(self):
        self.PATHTOSQLDIR=Util.OSUtil.getOSDBPath()
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/LoginDetails.db')
        #Creates a cursor to the database
        self.cur=self.con.cursor()
        self.todays_date = datetime.now().date()
        self.create_login_details_table()

    def create_login_details_table(self):
        self.cur.execute(
            "CREATE TABLE if not exists login_details(website_name, username, password, date_created)"
        )

    def add_entry_to_db(self,website_name,username,password):
        if self.website_password_set(website_name):
            self.update_entry_to_db(website_name,username,password)
        else:
            self.cur.execute(
                f'INSERT INTO login_details VALUES ("{website_name}","{username}","{password}","{self.todays_date}")'
            )
            self.con.commit()

    def update_entry_to_db(self,website_name,username,password):
        self.cur.execute('UPDATE login_details SET password = ?, username = ?, date_created = ? WHERE website_name = ?',
            (password, username, self.todays_date, website_name)
        )
        self.con.commit()
    
    def remove_entry_from_db(self,website_name):
        self.cur.execute(
            f'DELETE FROM login_details WHERE website_name = \'{website_name}\''
        )
        self.con.commit()

    def fetch_all_from_db(self):
        self.cur.execute(
            "SELECT * FROM login_details"
        )
        return self.cur.fetchall()

    def fetch_website_password(self,website_name):
        self.cur.execute(
            f'SELECT password FROM login_details WHERE website_name = \'{website_name}\''
        )
        return self.cur.fetchone()

    def website_password_set(self,website_name):
        password_set=False
        self.cur.execute(
            f'SELECT * FROM login_details WHERE website_name=\'{website_name}\''
        )
        if len(self.cur.fetchall()) >= 1:
            password_set=True
        return password_set

