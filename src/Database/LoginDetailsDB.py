import sqlite3

class LoginDetailsDB:
    def __init__(self):
        con=sqlite3.connect("Database/SQLFiles/LoginDetails.db")
