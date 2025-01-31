from selenium import webdriver
from Database.LoginDetailsDB import LoginDetailsDB
from WebsiteMonitorPopUp import *
import time
import requests

class WebsiteMonitor:
    def __init__(self):
        self.popup = WebsiteMonitorPopup.instance()
        self.currentURL = ""

    def run(self): 
        driver = webdriver.Chrome()
        while True:
            time.sleep(5)
            self.checkCurrentURL(driver.current_url)

    def checkCurrentURL(self, URL):
        if self.currentURL != URL and "login" in URL.lower():
            loginDetailsFound = False
            self.currentURL = URL
            loginDB = LoginDetailsDB()
            details = loginDB.fetchAllFromDB()
            r = requests.get(URL)
            for detail in details:
                if detail[0].lower() in URL.lower() or detail[0].lower() in r.text.lower():
                    loginDetailsFound = True
                    self.openPopup()
            if not loginDetailsFound:
                self.popup.showCreateLoginDetailsPopup()
        else:
            print("SKIPPED checkCurrentURL()")
            
    #DANGER: NOT WORKING YET AS THE PROGRAM IS UNABLE TO CREATE A POPUP OUTSIDE OF KIVY UI THREAD
    def openPopup(self):
        self.popup.showPopup("TESTING TITLE","TESTING CONTENT")