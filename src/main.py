from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from loginDetailsStorage import LoginDetailsStorage
from menu import *
from passwordGeneration import *
from passwordSearch import *

class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(Menu(name='Menu Screen'))
        self.screenManager.add_widget(LoginDetailsStorage(name="Login Details Storage Screen"))
        self.screenManager.add_widget(PasswordGeneration(name='Password Generation Screen'))
        self.screenManager.add_widget(PasswordSearch(name='Password Search Screen'))
        self.screenManager.current = 'Menu Screen' 
        return self.screenManager

if __name__ == '__main__':
    Main().run()