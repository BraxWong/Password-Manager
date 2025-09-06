import unittest
import Util.Util as util
import Database.LoginDetailsDB as loginDetailsDB
import time
import datetime
class UtilTestMethods(unittest.TestCase):

    def run_all_tests(self):
        print("\n")
        self.testsRan = 0
        self.testsPassed = 0
        self.testsFailed = 0
        testStartTime = time.perf_counter()
        self.test_dateComparison()
        self.test_generatePassword()
        self.test_checkPasswordInDB()
        testEndTime = time.perf_counter()
        print(f"\n\nTESTS RAN: {self.testsRan}\nTESTS PASSED: {self.testsPassed}\nTESTS FAILED: {self.testsFailed}\nTESTS RUNTIME: {testEndTime-testStartTime:0.4f} seconds\n\n")

    def test_dateComparison(self):
        try:
            safeDate = datetime.datetime.today() + datetime.timedelta(days=-1)
            safeDate = safeDate.strftime('%Y-%m-%d')
            self.assertEqual(("checkbox-marked-circle",[39/256,174/256,96/256,1],"Safe"),util.dateComparison(safeDate))
            print("test_dateComparison TEST 1: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1

        self.testsRan+=1
        try:
            cautionDate = datetime.datetime.today() + datetime.timedelta(days=-16)
            cautionDate = cautionDate.strftime('%Y-%m-%d')
            self.assertEqual(("alert",[255/256,165/256,0,1],"Caution"),util.dateComparison(cautionDate))
            print("test_dateComparison TEST 2: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1

        self.testsRan+=1
        try:
            dangerDate = datetime.datetime.today() + datetime.timedelta(days=-31)
            dangerDate = dangerDate.strftime('%Y-%m-%d')
            self.assertEqual(("alert-circle",[1,0,0,1],"Danger"),util.dateComparison(dangerDate))
            print("test_dateComparison TEST 3: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1

        self.testsRan+=1

    def test_generatePassword(self):
        try:
            passwordOne = util.generatePassword(True,14)
            self.assertEqual(True,self.test_passwordValidity(True,14,passwordOne))
            print("test_generatePassword TEST 1: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            passwordTwo = util.generatePassword(False,10)
            self.assertEqual(True,self.test_passwordValidity(False,10,passwordTwo))
            print("test_generatePassword TEST 2: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            passwordThree = util.generatePassword(False,8)
            self.assertEqual(True,self.test_passwordValidity(False,8,passwordThree))
            print("test_generatePassword TEST 3: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1


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
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            loginDetailsdb.addEntryToDB("TESTING1Website","TESTING1USERNAME","TESTINGPASSWORD")
            self.assertEqual(False,util.checkPasswordInDB("TESTINGPASSWORD1"))
            loginDetailsdb.removeEntryFromDB("TESTING1Website")
            print("test_checkPasswordInDB TEST 2: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            loginDetailsdb.addEntryToDB("TESTING1Website","TESTING1USERNAME","TESTING2PASSWORD")
            self.assertEqual(True,util.checkPasswordInDB("TESTING2PASSWORD"))
            loginDetailsdb.removeEntryFromDB("TESTING1Website")
            print("test_checkPasswordInDB TEST 3: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1
