from kivy.app import App
from menu import *

class Main(App):
    def build(self):
        return Menu()

if __name__ == '__main__':
    Main().run()
