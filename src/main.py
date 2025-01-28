from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from loginDetailsStorage import LoginDetailsStorage
from menu import *
from passwordGeneration import *
from passwordSearch import *
from WebsiteMonitor import *
import threading

class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(Menu(name='Menu Screen'))
        self.screenManager.add_widget(LoginDetailsStorage(name="Login Details Storage Screen"))
        self.screenManager.add_widget(PasswordGeneration(name='Password Generation Screen'))
        self.screenManager.add_widget(PasswordSearch(name='Password Search Screen'))
        self.screenManager.current = 'Menu Screen' 
        self.websiteMonitor = WebsiteMonitor()
        Clock.schedule_once(self.startWebsiteMonitorThread, 0)
        return self.screenManager

    def startWebsiteMonitorThread(self, dt):
        websiteMonitorThread = threading.Thread(target=self.websiteMonitor.run, daemon=True)
        websiteMonitorThread.start()

if __name__ == '__main__':
    Main().run()