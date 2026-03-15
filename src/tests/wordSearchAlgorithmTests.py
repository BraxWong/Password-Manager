import unittest
import Util.wordSearchAlgorithm as wordSearch
import Database.LoginDetailsDB as loginDetails
import time

class WordSearchAlgorithmTestMethods(unittest.TestCase):

    def run_all_tests(self):
        print("\n")
        self.testsRan = 0
        self.testsPassed = 0
        self.testsFailed = 0
        testStartTime = time.perf_counter()
        self.test_searchWebsite()
        testEndTime = time.perf_counter()
        print(f"\n\nTESTS RAN: {self.testsRan}\nTESTS PASSED: {self.testsPassed}\nTESTS FAILED: {self.testsFailed}\nTESTS RUNTIME: {testEndTime-testStartTime:0.4f} seconds\n\n")

    def test_searchWebsite(self):
        try:
            testOneWebsiteList = [loginDetails.LoginDetails("Google", None, None, None, None, None),
                                  loginDetails.LoginDetails("Netflix",None,None,None,None,None),
                                  loginDetails.LoginDetails("Amazon",None,None,None,None,None),
                                  loginDetails.LoginDetails("GPL",None,None,None,None,None),
                                  loginDetails.LoginDetails("Yahoo",None,None,None,None,None)]
            testOneUserInput = "Google"
            testOneResult = wordSearch.search_website(testOneWebsiteList,testOneUserInput)
            self.assertTrue(testOneResult[0],6)
            self.assertIsInstance(testOneResult,list)
            self.assertTrue(len(testOneResult))
            print("test_searchWebsite TEST 1: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1
   
        try:
            testTwoWebsiteList = [loginDetails.LoginDetails("Google", None, None, None, None, None),
                                  loginDetails.LoginDetails("Netflix",None,None,None,None,None),
                                  loginDetails.LoginDetails("Amazon",None,None,None,None,None),
                                  loginDetails.LoginDetails("GPL",None,None,None,None,None),
                                  loginDetails.LoginDetails("Yahoo",None,None,None,None,None)]
            testTwoUserInput = "gpl"
            testTwoResult = wordSearch.search_website(testTwoWebsiteList,testTwoUserInput)
            self.assertTrue(testTwoResult[3],3)
            self.assertIsInstance(testTwoResult,list)
            self.assertTrue(len(testTwoResult),5)
            print("test_searchWebsite TEST 2: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            testThreeWebsiteList = [loginDetails.LoginDetails("Google", None, None, None, None, None),
                                  loginDetails.LoginDetails("Netflix",None,None,None,None,None),
                                  loginDetails.LoginDetails("Amazon",None,None,None,None,None),
                                  loginDetails.LoginDetails("GPL",None,None,None,None,None),
                                  loginDetails.LoginDetails("Yahoo",None,None,None,None,None)]
            testThreeUserInput = "amaZoN"
            testThreeResult = wordSearch.search_website(testThreeWebsiteList,testThreeUserInput)
            self.assertTrue(testThreeResult[2],6)
            self.assertIsInstance(testThreeResult,list)
            self.assertTrue(len(testThreeResult),5)
            print("test_searchWebsite TEST 3: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1