from datetime import datetime
from Database.LoginDetailsDB import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
import random
import platform
import os

def getOSDBPath():
    OS = platform.system()
    DBDirectory = "Database/SQLFiles"
    if OS == "Darwin":
        DBDirectory = f"/tmp/{DBDirectory}"
    elif OS == "Windows":
        DBDirectory = f"C:/{DBDirectory}"
    else:
        DBDirectory = f"/var/tmp/{DBDirectory}"
    if not os.path.exists(DBDirectory):
        os.makedirs(DBDirectory,exist_ok=True)
    migrateDB(DBDirectory)
    return DBDirectory

def migrateDB(DBDirectory):
    if os.path.isfile("Database/SQLFiles/EmailSettings.db"):
        os.rename("Database/SQLFiles/EmailSettings.db", DBDirectory + "/EmailSettings.db")
    if os.path.isfile("Database/SQLFiles/LoginDetails.db"):
        os.rename("Database/SQLFiles/LoginDetails.db", DBDirectory + "/LoginDetails.db")
    if os.path.isfile("Database/SQLFiles/VerifyUser.db"):
        os.rename("Database/SQLFiles/VerifyUser.db", DBDirectory + "/VerifyUser.db")

def dateComparison(date):
    todays_date = datetime.now().date()         
    date_format = '%Y-%m-%d'
    date = datetime.strptime(date,date_format).date()
    difference = (todays_date - date).days
    if difference < 15:
        return ("checkbox-marked-circle",[39/256,174/256,96/256,1],"Safe")
    elif difference > 15 and difference < 30:
        return ("alert",[255/256,165/256,0,1],"Caution")
    else:
        return ("alert-circle",[1,0,0,1],"Danger")

def generatePassword(specialSymbolEnabled,passwordLength):
        numbers=['0','1','2','3','4','5','6','7','8','9']
        numberExistsInPassword=False
        letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        lettersExistsInPassword=False
        upperLetters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        upperLettersExistsInPassword=False
        symbols=['!','@','#','$','^','&','*','?']
        symbolExistsInPassword=False
        password=''
        for i in range(passwordLength):
            if specialSymbolEnabled:
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

        if numberExistsInPassword and lettersExistsInPassword and upperLettersExistsInPassword and symbolExistsInPassword and not checkPasswordInDB(password):
            return password
        return generatePassword(specialSymbolEnabled,passwordLength)

def checkPasswordInDB(generatedPassword):
    passwordFoundInDB = False
    loginDetailsDB = LoginDetailsDB()
    allPassword = loginDetailsDB.fetchAllFromDB()
    for password in allPassword:
        if generatedPassword == password[2]:
            passwordFoundInDB = True
    return passwordFoundInDB

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