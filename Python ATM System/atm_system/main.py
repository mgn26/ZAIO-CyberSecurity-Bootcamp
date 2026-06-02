"""Welcome to the python ATM System."""
from program.register import Register
from program.login import Login


main_display = "\n============================\n" \
    "Welcome to PyBank ATM\n" \
    "============================\n" \
    "1. Register\n" \
    "2. Login\n" \
    "3. Exit\n"

option = 0

while option != 3:
    print(main_display)
    option = int(input("Select an option: "))
    if (option == 1):
        print("\n--- Account Registration ---")
        registration = Register()
        registration.create_account()
    elif (option == 2):
        print("\n--- Login ---")
        login = Login()

    elif (option > 3 or option < 1):
        print("\nPlease choose a valid option.")

print("\nExiting Program. Good Bye!")
