import tests.UtilTests as utilTests
import tests.passwordHashingTests as hashingTests
import tests.wordSearchAlgorithmTests as wordSearchTests
import tests.LastActionTakenTests as last_action_taken_tests
while True:
    print("Here is a list of tests you can run:\nPress 1: Util Tests\nPress 2: Password Hashing Tests\nPress 3: Word Search Algorithm Tests\nPress 4: Run Last Action Taken Tests\nPress 5: Run All Tests\nPress ANY key: Quit")
    userInput = input()
    if userInput == "1":
        test_instance = utilTests.UtilTestMethods()
        test_instance.run_all_tests()
    elif userInput == "2":
        test_instance = hashingTests.PasswordHashingTestMethods()
        test_instance.run_all_tests()
    elif userInput == "3":
        test_instance = wordSearchTests.WordSearchAlgorithmTestMethods()
        test_instance.run_all_tests()
    elif userInput == "4":
        test_instance = last_action_taken_tests.LastActionTakenTestMethods()
        test_instance.run_all_tests()
    elif userInput == "5":
        test_instance = utilTests.UtilTestMethods()
        test_instance.run_all_tests()
        test_instance = hashingTests.PasswordHashingTestMethods()
        test_instance.run_all_tests()
        test_instance = wordSearchTests.WordSearchAlgorithmTestMethods()
        test_instance.run_all_tests()
        test_instance = last_action_taken_tests.LastActionTakenTestMethods()
        test_instance.run_all_tests()
    else:
        break
