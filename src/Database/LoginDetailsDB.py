import mysql.connector

class LoginDetailsDB:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="username",
            password="password"
        )
        print(self.mydb)
