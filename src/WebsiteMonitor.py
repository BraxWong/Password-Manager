from selenium import webdriver
from Database.LoginDetailsDB import LoginDetailsDB
from WebsiteMonitorPopUp import *
import time
class WebsiteMonitor:
    def __init__(self):
        self.popup = WebsiteMonitorPopup.instance()

    def run(self): 
        try:
            driver = webdriver.Chrome()
            while True:
                time.sleep(5)
                self.openPopup()
        except Exception as e:
            print(f"Monitoring error: {e}")
        finally:
            if 'driver' in locals():
                driver.quit()

    #DANGER: NOT WORKING YET AS THE PROGRAM IS UNABLE TO CREATE A POPUP OUTSIDE OF KIVY UI THREAD
    def openPopup(self):
        self.popup.showPopup("TESTING TITLE","TESTING CONTENT")