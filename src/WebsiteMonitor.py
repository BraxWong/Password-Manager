from selenium import webdriver
from Database.LoginDetailsDB import LoginDetailsDB
from WebsiteMonitorPopUp import *
import time
import requests

class WebsiteMonitor:
    def __init__(self):
        self.popup = WebsiteMonitorPopup.instance()
        self.currentURL = ""
        self.driver = None

    def run(self): 
        try:
            self.driver = webdriver.Chrome()
            while True:
                if self.driver != None:
                    time.sleep(5)
                    self.checkCurrentURL(self.driver.current_url)
        except Exception as e:
            pass

    def stop(self):
        self.driver.quit()
        self.driver = None

    #TODO: Something weird is going on here with the database race condition. It would not run showCreateLoginDetailsPopup() even if the record of the website has been removed from the database.
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
                    self.openPopup(detail[0],detail[1],detail[2])
            if not loginDetailsFound:
                self.popup.showCreateLoginDetailsPopup()
            
    def openPopup(self,websiteName,username,password):
        self.popup.showPopup(f"{websiteName}'s login details",f"Username: {username}\nPassword: {password}")