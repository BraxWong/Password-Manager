from selenium import webdriver
class WebsiteMonitor:
    def __init__(self):
        driver = webdriver.Chrome()
        while(True):
            print(driver.current_url)
            pass
