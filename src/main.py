from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from menu import *
from passwordGeneration import *
from passwordSearch import *

class Main(App):
    def build(self):
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(Menu(name='Menu Screen'))
        self.screenManager.add_widget(PasswordGeneration(name='Password Generation Screen'))
        self.screenmanager.add_widget(PasswordSearch(name='Password Search Screen'))
        self.screenManager.current = 'Menu Screen' 
        return self.screenManager

if __name__ == '__main__':
    Main().run()
