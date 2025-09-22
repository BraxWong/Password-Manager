import sqlite3
from datetime import datetime
import Util.OSUtil

class LoginDetails:
    def __init__(self, website_name, username, password, date_created, update_url):
        self.website_name = website_name
        self.username = username
        self.password = password
        self.date_created = date_created
        self.update_url = update_url

class LoginDetailsDB:
    def __init__(self):
        self.PATHTOSQLDIR=Util.OSUtil.getOSDBPath()
        self.con=sqlite3.connect(self.PATHTOSQLDIR+'/LoginDetails.db')
        #Creates a cursor to the database
        self.cur=self.con.cursor()
        self.todays_date = datetime.now().date()
        self.create_login_details_table()
        self.update_login_details_table()

    def create_login_details_table(self):
        self.cur.execute(
            "CREATE TABLE if not exists login_details(website_name, username, password, date_created)"
        )

    def update_login_details_table(self):
        #Retrieves table schema info
        self.cur.execute(
            "PRAGMA table_info(login_details)"
        )
        columns = [column[1] for column in self.cur.fetchall()]
        if 'update_url' not in columns:
            self.cur.execute(
                "ALTER TABLE login_details ADD COLUMN update_url"
            )
            self.con.commit()

    def add_entry_to_db(self,website_name,username,password,update_url):
        if self.website_password_set(website_name):
            self.update_entry_to_db(website_name,username,password,update_url)
        else:
            self.cur.execute(
                f'INSERT INTO login_details VALUES ("{website_name}","{username}","{password}","{self.todays_date}","{update_url}")'
            )
            self.con.commit()

    def update_entry_to_db(self,website_name,username,password,update_url):
        self.cur.execute('UPDATE login_details SET password = ?, username = ?, date_created = ?, update_url = ? WHERE website_name = ?',
            (password, username, self.todays_date, update_url, website_name)
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
        user_data = self.cur.fetchall()
        credentials = [
            LoginDetails(website_name, username, password, date_created, update_url) 
            for website_name, username, password, date_created, update_url in user_data
        ]
        return credentials

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

    def fetch_password_update_website(self,website_name):
        self.cur.execute(
            f'SELECT update_url FROM login_details WHERE website_name = \'{website_name}\''
        )
        return self.cur.fetchone()

