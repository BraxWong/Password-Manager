from selenium import webdriver
from Database.LoginDetailsDB import LoginDetailsDB
from WebsiteMonitorPopUp import *
import time
import requests

class WebsiteMonitor:
    def __init__(self):
        self.popup = WebsiteMonitorPopup.instance()
        self.current_url = ""
        self.driver = None

    def run(self): 
        try:
            self.driver = webdriver.Chrome()
            while True:
                if self.driver != None:
                    time.sleep(5)
                    self.check_current_url(self.driver.current_url)
        except Exception as e:
            pass

    def stop(self):
        self.driver.quit()
        self.driver = None

    #TODO: Something weird is going on here with the database race condition. It would not run showCreateLoginDetailsPopup() even if the record of the website has been removed from the database.
    def check_current_url(self, URL):
        if self.current_url != URL and "login" in URL.lower():
            login_details_found = False
            self.current_url = URL
            login_db = LoginDetailsDB()
            details = login_db.fetchAllFromDB()
            r = requests.get(URL)
            for detail in details:
                if detail[0].lower() in URL.lower() or detail[0].lower() in r.text.lower():
                    login_details_found = True
                    self.openPopup(detail[0],detail[1],detail[2])
            if not login_details_found:
                self.popup.showCreateLoginDetailsPopup()
            
    def openPopup(self,websiteName,username,password):
        self.popup.showPopup(f"{websiteName}'s login details",username,password)