from datetime import datetime
from Database.LoginDetailsDB import *
import random

def check_2FA_code(user_code, auth_system, popUp, callback):
    if not auth_system.auth_expired() and user_code == auth_system.code: 
        popUp.dismiss()
        callback(True) 
    else:
        callback(False)

def date_comparison(date):
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

def generate_password(special_symbol_enabled,password_length):
        numbers=['0','1','2','3','4','5','6','7','8','9']
        number_exists_in_password=False
        letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        letters_exists_in_password=False
        upper_letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        upper_letters_exists_in_password=False
        symbols=['!','@','#','$','^','&','*','?']
        symbol_exists_in_password=False
        password=''
        for i in range(password_length):
            if special_symbol_enabled:
                num=random.randrange(0,4)
            else:
                num=random.randrange(0,3)
                symbol_exists_in_password=True

            match num:
                case 0:
                    password+=random.choice(numbers)
                    number_exists_in_password=True
                case 1:
                    password+=random.choice(letters)
                    letters_exists_in_password=True
                case 2:
                    password+=random.choice(upper_letters)
                    upper_letters_exists_in_password=True
                case 3:
                    password+=random.choice(symbols)
                    symbol_exists_in_password=True

        if number_exists_in_password and letters_exists_in_password and upper_letters_exists_in_password and symbol_exists_in_password and not check_password_in_db(password):
            return password
        return generate_password(special_symbol_enabled,password_length)

def check_password_in_db(generated_password):
    password_found_in_db = False
    login_details_db = LoginDetailsDB()
    all_password = login_details_db.fetch_all_from_db()
    for user_credentials in all_password:
        if generated_password == user_credentials.password:
            password_found_in_db = True
    return password_found_in_db
