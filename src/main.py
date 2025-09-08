from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from loginDetailsStorage import LoginDetailsStorage
from menu import *
from passwordGeneration import *
from passwordSearch import *
from TwoFactorAuthentication import *

class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Menu(name='Menu Screen'))
        self.screen_manager.add_widget(LoginDetailsStorage(name="Login Details Storage Screen"))
        self.screen_manager.add_widget(PasswordGeneration(name='Password Generation Screen'))
        self.screen_manager.add_widget(PasswordSearch(name='Password Search Screen'))
        self.screen_manager.add_widget(TwoFactorAuthentication(name='2FA Screen'))
        self.screen_manager.current = 'Menu Screen' 
        return self.screen_manager

if __name__ == '__main__':
    Window.size = (1200,900)
    Main().run()
