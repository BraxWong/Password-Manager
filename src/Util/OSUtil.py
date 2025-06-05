import platform
import os

def getOSDBPath():
    OS = platform.system()
    DBDirectory = "Database/SQLFiles"
    if OS == "Darwin":
        DBDirectory = f"/tmp/{DBDirectory}"
    elif OS == "Windows":
        DBDirectory = f"C:/{DBDirectory}"
    else:
        DBDirectory = f"/var/tmp/{DBDirectory}"
    if not os.path.exists(DBDirectory):
        os.makedirs(DBDirectory,exist_ok=True)
    migrateDB(DBDirectory)
    return DBDirectory

def migrateDB(DBDirectory):
    if os.path.isfile("Database/SQLFiles/EmailSettings.db"):
        os.rename("Database/SQLFiles/EmailSettings.db", DBDirectory + "/EmailSettings.db")
    if os.path.isfile("Database/SQLFiles/LoginDetails.db"):
        os.rename("Database/SQLFiles/LoginDetails.db", DBDirectory + "/LoginDetails.db")
    if os.path.isfile("Database/SQLFiles/VerifyUser.db"):
        os.rename("Database/SQLFiles/VerifyUser.db", DBDirectory + "/VerifyUser.db")

