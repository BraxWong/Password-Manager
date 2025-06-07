from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

def createLoginDetailPopupLayout():
    mainLayout = BoxLayout(
                orientation='vertical',
                size_hint=(1, 1),  
                padding=0,
                spacing=50 
            )
    applicationNameLayout = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height='50dp',
        spacing='10dp'
    )
    applicationNameLayout.add_widget(
        Label(
            text='Name of application/website',
            font_size='15sp',
            size_hint_x=0.4
        )
    )
    applicationNameTextInput = TextInput(
        text='', multiline=False, size_hint=(0.6, None), height='40dp'
    )
    applicationNameLayout.add_widget(applicationNameTextInput)
    mainLayout.add_widget(applicationNameLayout)

            
    usernameLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
    usernameLayout.add_widget(
        Label(text='Username', font_size='15sp', size_hint_x=0.4)
    )
    usernameTextInput = TextInput(
        text='', multiline=False, size_hint=(0.6, None), height='40dp'
    )
    usernameLayout.add_widget(usernameTextInput)
    mainLayout.add_widget(usernameLayout)

    passwordLengthLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp', spacing='10dp')
    passwordLengthLayout.add_widget(
        Label(text='Length of password', font_size='15sp', size_hint_x=0.4)
    )
    passwordSliderLayout = BoxLayout(orientation='vertical', size_hint_x=0.6)
    passwordLengthLabel = Label(text='14', font_size='20sp', halign='center')
    passwordSliderLayout.add_widget(passwordLengthLabel)
    passwordLengthSlider = Slider(
        min=1, max=64, value=14, value_track=True, value_track_color=[1, 0, 0, 1]
    )
    passwordLengthSlider.bind(value=lambda instance, value:onSliderValueChange(value,passwordLengthLabel))
    passwordSliderLayout.add_widget(passwordLengthSlider)
    passwordLengthLayout.add_widget(passwordSliderLayout)
    mainLayout.add_widget(passwordLengthLayout)

    symbolLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
    symbolLayout.add_widget(
        Label(text='Include special symbol', font_size='15sp', size_hint_x=0.135)
    )
    symbolEnabledCheckBox = CheckBox(size_hint_x=0.2)
    symbolLayout.add_widget(symbolEnabledCheckBox)
    mainLayout.add_widget(symbolLayout)
    return {"Layout": mainLayout, "ApplicationName": applicationNameTextInput, "Username": usernameTextInput, "SymbolEnabledCheckBox": symbolEnabledCheckBox, "PasswordLength": passwordLengthSlider}

def onSliderValueChange(val,passwordLengthLabel):
    passwordLengthLabel.text = str(int(val))
