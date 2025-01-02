from selenium import webdriver
from Database.LoginDetailsDB import LoginDetailsDB
class WebsiteMonitor:
    def __init__(self):
        loginDetailsDB = LoginDetailsDB()
        print(loginDetailsDB.fetchAllFromDB())
        # driver = webdriver.Chrome()
        # while(True):
        #     print(driver.current_url)
        #     pass
