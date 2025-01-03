from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from loginDetailsStorage import LoginDetailsStorage
from menu import *
from passwordGeneration import *
from passwordSearch import *
from WebsiteMonitor import *

class Main(App):
    def build(self):
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(Menu(name='Menu Screen'))
        self.screenManager.add_widget(LoginDetailsStorage(name="Login Details Storage Screen"))
        self.screenManager.add_widget(PasswordGeneration(name='Password Generation Screen'))
        self.screenManager.add_widget(PasswordSearch(name='Password Search Screen'))
        self.screenManager.current = 'Menu Screen' 
        return self.screenManager

if __name__ == '__main__':
    # website_monitor = WebsiteMonitor()
    Main().run()
