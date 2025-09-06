from datetime import datetime
from Database.LoginDetailsDB import *
import random

def check_2FA_code(user_code, auth_system, popUp, callback):
    if not auth_system.auth_expired() and user_code == auth_system.code: 
        popUp.dismiss()
        callback(True) 
    else:
        callback(False)

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
