"""
This module implement the transactions class used in PyBank ATM.
"""

class Transaction:
    """
    This class handles all operations associated with performing transactions.
    """
    def __init__(self):
        pass

    def transact(self):
        while True:
            print(self.main_menu())
            option = int(input("Select an option: "))
            if (option == 1):
                print("\n--- Withdraw ---")
                
            elif (option == 2):
                print("\n--- Deposit ---")

            elif (option == 3):
                print("\n--- EFT Transfer ---")

            elif (option == 4):
                print("\n--- Statement ---")
                
            elif (option == 5):
                print("\nLogged out. Stay safe.")
                break
            else:
                print("\nPlease choose a valid option.")

    def withdraw():
        pass

    def deposit():
        pass

    def transfer():
        pass

    def view_statement():
        pass

    def main_menu(self):
        main_menu = "1. Withdraw\n" \
        "2. Deposit\n" \
        "3. Transfer (EFT)\n" \
        "4. View Statement\n" \
        "5. Logout\n"
        return main_menu
