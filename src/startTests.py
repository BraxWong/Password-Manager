import tests.UtilTests as utilTests
import tests.passwordHashingTests as hashingTests

#     ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
#     ┃                                                                    ┃
#     ┃ TODO: Create a CLI tool so users (Me) can decide what tests to run ┃
#     ┃                                                                    ┃
#     ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

while True:
    print("Here is a list of tests you can run:\nPress 1: Util Tests\nPress 2: Password Hashing Tests\nPress 3: Word Search Algorithm Tests\nPress 4: UI Tests\nPress ANY key: Quit")
    userInput = input()
    if userInput == "1":
        test_instance = utilTests.UtilTestMethods()
        test_instance.run_all_tests()
    elif userInput == "2":
        test_instance = hashingTests.PasswordHashingTestMethods()
        test_instance.run_all_tests()
    elif userInput == "3":
        pass
    elif userInput == "4":
        pass
    else:
        break
