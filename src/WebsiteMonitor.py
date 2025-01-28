from selenium import webdriver
from Database.LoginDetailsDB import LoginDetailsDB
import time
class WebsiteMonitor:
    def __init__(self):
        pass

    def run(self): 
        try:
            driver = webdriver.Chrome()
            while True:
                time.sleep(5)
                print(driver.current_url)
        except Exception as e:
            print(f"Monitoring error: {e}")
        finally:
            if 'driver' in locals():
                driver.quit()
