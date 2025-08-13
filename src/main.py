from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from loginDetailsStorage import LoginDetailsStorage
from menu import *
from passwordGeneration import *
from passwordSearch import *
from emailNotification import *

class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(Menu(name='Menu Screen'))
        self.screenManager.add_widget(LoginDetailsStorage(name="Login Details Storage Screen"))
        self.screenManager.add_widget(PasswordGeneration(name='Password Generation Screen'))
        self.screenManager.add_widget(PasswordSearch(name='Password Search Screen'))
        self.screenManager.add_widget(EmailNotification(name='Email Notification Screen'))
        self.screenManager.current = 'Menu Screen' 
        return self.screenManager

if __name__ == '__main__':
    Window.size = (1200,900)
    Main().run()