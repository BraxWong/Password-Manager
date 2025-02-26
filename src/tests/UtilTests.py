from sys import exception
import unittest
import Util.Util as util
import Database.LoginDetailsDB as loginDetailsDB
class UtilTestMethods(unittest.TestCase):

    def run_all_tests(self):
        self.test_dateComparison()
        self.test_generatePassword()
        self.test_checkPasswordInDB()


# ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
# ┃                                                                              ┃
# ┃      WARNING: This test case will pass for now but figure out a way to       ┃
# ┃       convert today's date to string, then subtract 15 days to get the       ┃
# ┃        caution result and more than 30 days to get the danger result.        ┃
# ┃                                                                              ┃
# ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

    def test_dateComparison(self):
        try:
            self.assertEqual(("checkbox-marked-circle",[39/256,174/256,96/256,1],"Safe"),util.dateComparison("2025-02-24"))
            print("test_dateComparison TEST 1: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

        try:
            self.assertEqual(("alert",[255/256,165/256,0,1],"Caution"),util.dateComparison("2025-02-01"))
            print("test_dateComparison TEST 2: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

        try:
            self.assertEqual(("alert-circle",[1,0,0,1],"Danger"),util.dateComparison("2025-01-01"))
            print("test_dateComparison TEST 3: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

    def test_generatePassword(self):
        try:
            passwordOne = util.generatePassword(True,14)
            self.assertEqual(True,self.test_passwordValidity(True,14,passwordOne))
            print("test_generatePassword TEST 1: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

        try:
            passwordTwo = util.generatePassword(False,10)
            self.assertEqual(True,self.test_passwordValidity(False,10,passwordTwo))
            print("test_generatePassword TEST 2: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

        try:
            passwordThree = util.generatePassword(False,8)
            self.assertEqual(True,self.test_passwordValidity(False,8,passwordThree))
            print("test_generatePassword TEST 3: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")


    def test_passwordValidity(self,specialSymbolEnabled,passwordLength,password):
        validPasswordLength = len(password)==passwordLength
        if specialSymbolEnabled:
            symbols=['!','@','#','$','^','&','*','?']
            foundSymbol = False
            for symbol in symbols:
                if symbol in password:
                    foundSymbol = True
            return (foundSymbol == True) and (validPasswordLength == True) 
        return validPasswordLength 

    def test_checkPasswordInDB(self):
        loginDetailsdb = loginDetailsDB.LoginDetailsDB()
        try:
            loginDetailsdb.addEntryToDB("TESTING1Website","TESTING1USERNAME","TESTINGPASSWORD")
            self.assertEqual(True,util.checkPasswordInDB("TESTINGPASSWORD"))
            loginDetailsdb.removeEntryFromDB("TESTING1Website")
            print("test_checkPasswordInDB TEST 1: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

        try:
            loginDetailsdb.addEntryToDB("TESTING1Website","TESTING1USERNAME","TESTINGPASSWORD")
            self.assertEqual(False,util.checkPasswordInDB("TESTINGPASSWORD1"))
            loginDetailsdb.removeEntryFromDB("TESTING1Website")
            print("test_checkPasswordInDB TEST 2: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

        try:
            loginDetailsdb.addEntryToDB("TESTING1Website","TESTING1USERNAME","TESTING2PASSWORD")
            self.assertEqual(True,util.checkPasswordInDB("TESTING2PASSWORD"))
            loginDetailsdb.removeEntryFromDB("TESTING1Website")
            print("test_checkPasswordInDB TEST 3: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

