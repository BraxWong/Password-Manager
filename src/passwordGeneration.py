from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

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
        
    #TODO: implement the following function to generate a password
    def generatePassword(self,widget):
        pass
        
