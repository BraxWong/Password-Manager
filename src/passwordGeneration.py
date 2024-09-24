from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
import random

class PasswordGeneration(Screen):

    def __init__(self, **kwargs):
        super(PasswordGeneration,self).__init__(**kwargs)
        self.mainLayout = BoxLayout(orientation='vertical')
        self.mainLayout.add_widget(Label(text='Create a Password',font_size='20sp'))

        self.applicationNameLayout = BoxLayout(orientation='horizontal')
        self.applicationNameLayout.add_widget(Label(text='Name of applcation/website',
                                                    font_size='15sp',
                                                    pos_hint={'x':0.2,'y':0},))
        self.applicationNameTextInput = TextInput(text='Name of the applcation or website', 
                                                  multiline=False, 
                                                  size_hint=(None,None), 
                                                  height=30, 
                                                  width=250,
                                                  pos_hint={'x':0.5,'y':0.45})
        self.applicationNameLayout.add_widget(self.applicationNameTextInput)
        self.mainLayout.add_widget(self.applicationNameLayout)

        self.generatePasswordButton = Button(text='Generate a password',
                                             size_hint=(None,None),
                                             height=20,
                                             width=200,
                                             pos_hint={'x':0.379,'y':0.5})
        self.generatePasswordButton.bind(on_press=self.generatePassword)
        self.mainLayout.add_widget(self.generatePasswordButton)
        self.add_widget(self.mainLayout)
        
    def generatePassword(self,widget):
        numbers=['0','1','2','3','4','5','6','7','8','9']
        numberExistsInPassword=False
        letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        lettersExistsInPassword=False
        upperLetters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        upperLettersExistsInPassword=False
        symbols=['!','@','#','$','^','&','*','?']
        symbolExistsInPassword=False
        password=''
        for i in range(14):
            num=random.randrange(0,4)
            if num==0:
                password+=random.choice(numbers)
                numberExistsInPassword=True
            elif num==1:
                password+=random.choice(letters)
                lettersExistsInPassword=True
            elif num==2:
                password+=random.choice(upperLetters)
                upperLettersExistsInPassword=True
            else:
                password+=random.choice(symbols)
                symbolExistsInPassword=True
        if numberExistsInPassword and lettersExistsInPassword and upperLettersExistsInPassword and symbolExistsInPassword:
            return password
        return self.generatePassword(widget)


        
