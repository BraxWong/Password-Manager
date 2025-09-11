import platform
import os

def getOSDBPath():
    OS = platform.system()
    db_directory = "Database/SQLFiles"
    if OS == "Darwin":
        db_directory = f"/tmp/{db_directory}"
    elif OS == "Windows":
        db_directory = f"C:/{db_directory}"
    else:
        db_directory = f"/var/tmp/{db_directory}"
    if not os.path.exists(db_directory):
        os.makedirs(db_directory,exist_ok=True)
    migrateDB(db_directory)
    return db_directory

def migrateDB(db_directory):
    if os.path.isfile("Database/SQLFiles/EmailSettings.db"):
        os.rename("Database/SQLFiles/EmailSettings.db", db_directory + "/EmailSettings.db")
    if os.path.isfile("Database/SQLFiles/LoginDetails.db"):
        os.rename("Database/SQLFiles/LoginDetails.db", db_directory + "/LoginDetails.db")
    if os.path.isfile("Database/SQLFiles/VerifyUser.db"):
        os.rename("Database/SQLFiles/VerifyUser.db", db_directory + "/VerifyUser.db")

