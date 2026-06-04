"""
This module implement the transactions class used in PyBank ATM.
"""
from .file_operation import *  # file_operation just contains a few functions


class Transaction:
    """
    This class handles all operations associated with performing transactions.

    Attributes:
        acc_bal_file (str): 
        transact_file (str):
    """

    def __init__(self, accounts, active_acc):
        """
        Initializes Transaction object.
        """
        # This object will need to update file contents for both files.
        self.acc_bal_file = "account_balances.txt"
        self.transact_file = "transactions.txt"

        # Little more efficient passing accounts at the cost of robustness.
        self.accounts_balances = accounts
        self.transactions = load_from_file(self.transact_file)
        self.active_account = active_acc

    def __del__(self):
        """
        Saves this object's state to file before destruction.
        """
        # To ensure that the csv file that was loaded to memory
        # during construction is up to date with this object's state.
        save_to_file(self.acc_bal_file, self.accounts_balances)
        save_to_file(self.transact_file, self.transactions)

    def transact(self):
        while True:
            print(self.main_menu())
            option = int(input("Select an option: "))
            if (option == 1):
                print("\n--- Withdraw ---")
                self.withdraw()
            elif (option == 2):
                print("\n--- Deposit ---")
                self.deposit()
            elif (option == 3):
                print("\n--- EFT Transfer ---")

            elif (option == 4):
                print("\n--- Statement ---")
                
            elif (option == 5):
                print("\nLogged out. Stay safe.")
                break
            else:
                print("\nPlease choose a valid option.")

    def withdraw(self):
        """
        Subtracts a specified amount from balance.
        """
        input_amount = float(input("\nAmount to Withdraw: R "))
        curr_balance = float(self.active_account["balance"])

        if (curr_balance < input_amount):
            print("\nInsufficient Funds.")
            return
        
        curr_balance -= input_amount

        for row in self.accounts_balances:
            if (self.active_account["phone_number"] == row["phone_number"]):
                row["balance"] = curr_balance

        save_to_file(self.acc_bal_file, self.accounts_balances)
        print(f"\nWithdrawal successful. New balance: R{curr_balance:.2f}")

    def deposit(self):
        """
        Adds a specified amount to balance.
        """
        input_amount = float(input("\nAmount to Deposit: R "))
        curr_balance = float(self.active_account["balance"])

        if (input_amount <= 0):
            print("\nInvalid amount.")
            return
        
        curr_balance += input_amount

        for row in self.accounts_balances:
            if (self.active_account["phone_number"] == row["phone_number"]):
                row["balance"] = curr_balance

        save_to_file(self.acc_bal_file, self.accounts_balances)
        print(f"\nDeposit successful. New balance: R{curr_balance:.2f}")

    def transfer():
        pass

    def view_statement():
        pass

    def main_menu(self):
        main_menu = "\n--- Main Menu ---\n" \
        "1. Withdraw\n" \
        "2. Deposit\n" \
        "3. Transfer (EFT)\n" \
        "4. View Statement\n" \
        "5. Logout\n"
        return main_menu
