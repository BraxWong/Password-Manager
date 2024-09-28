from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
import random
from Database.LoginDetailsDB import LoginDetailsDB  

class PasswordGeneration(Screen):

    def __init__(self, **kwargs):
        super(PasswordGeneration,self).__init__(**kwargs)
        self.db = LoginDetailsDB()
        self.mainLayout = BoxLayout(orientation='vertical')
        self.mainLayout.add_widget(Label(text='Create a Password',font_size='20sp'))

        self.applicationNameLayout = BoxLayout(orientation='horizontal')
        self.applicationNameLayout.add_widget(Label(text='Name of applcation/website',
                                                    font_size='15sp',
                                                    pos_hint={'x':0.2,'y':0},))
        self.applicationNameTextInput = TextInput(text='', 
                                                  multiline=False,
                                                  size_hint=(None,None), 
                                                  height=30, 
                                                  width=250,
                                                  pos_hint={'x':0.5,'y':0.45})
        self.applicationNameLayout.add_widget(self.applicationNameTextInput)
        self.mainLayout.add_widget(self.applicationNameLayout)

        self.passwordLengthLayout = BoxLayout(orientation='horizontal')
        self.passwordLengthLayout.add_widget(Label(text='Length of password',
                                                     font_size='15sp'))
        self.passwordSliderLayout = BoxLayout(orientation='vertical')
        self.passwordLengthLabel = Label(text='14', font_size='20sp')
        self.passwordSliderLayout.add_widget(self.passwordLengthLabel)
        self.passwordLengthSlider = Slider(min=1, 
                                           max=64, 
                                           value=14,
                                           value_track=True,
                                           value_track_color=[1,0,0,1])
        self.passwordLengthSlider.bind(value=self.onSliderValueChange)
        self.passwordSliderLayout.add_widget(self.passwordLengthSlider)
        self.passwordLengthLayout.add_widget(self.passwordSliderLayout)
        self.mainLayout.add_widget(self.passwordLengthLayout)

        self.symbolLayout = BoxLayout(orientation='horizontal')
        self.symbolLayout.add_widget(Label(text='Include special symbol',
                                           font_size='15sp'))
        self.symbolEnabledCheckBox = CheckBox()
        self.symbolLayout.add_widget(self.symbolEnabledCheckBox)
        self.mainLayout.add_widget(self.symbolLayout)

        self.generatePasswordButton = Button(text='Generate a password',
                                             size_hint=(None,None),
                                             height=20,
                                             width=200,
                                             pos_hint={'x':0.379,'y':0.2})
        self.generatePasswordButton.bind(on_press=self.generatePassword)
        self.mainLayout.add_widget(self.generatePasswordButton)
        self.add_widget(self.mainLayout)
       
    def onSliderValueChange(self,widget,val):
        self.passwordLengthLabel.text=str(int(val))

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
        for i in range(int(self.passwordLengthLabel.text)):
            if self.symbolEnabledCheckBox.active:
                num=random.randrange(0,4)
            else:
                num=random.randrange(0,3)
                symbolExistsInPassword=True

            match num:
                case 0:
                    password+=random.choice(numbers)
                    numberExistsInPassword=True
                case 1:
                    password+=random.choice(letters)
                    lettersExistsInPassword=True
                case 2:
                    password+=random.choice(upperLetters)
                    upperLettersExistsInPassword=True
                case 3:
                    password+=random.choice(symbols)
                    symbolExistsInPassword=True

        if numberExistsInPassword and lettersExistsInPassword and upperLettersExistsInPassword and symbolExistsInPassword:
            self.db.addEntryToDB(self.applicationNameTextInput.text, password)
            popup = Popup(title='Password Generated',
                          content=Label(text=f'Website:{self.applicationNameTextInput.text}\nPassword:{password}\nSaved in Database'),
                          size_hint=(None,None),
                          size=(400,400))
            popup.open()
            return password
        return self.generatePassword(widget)


        
