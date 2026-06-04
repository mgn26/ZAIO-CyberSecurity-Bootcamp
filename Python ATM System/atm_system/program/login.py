"""
This module implement the login class used in PyBank ATM.
"""
from .account_balance import AccountBalance
from .transaction import Transaction
from .str_gen import acc_num_gen, rand_str_gen
from .pin_hasher import pin_hasher
from .file_operation import *  # file_operation just contains a few functions


class Login:
    """
    This class handles all operations associated with account management.
    """
    def __init__(self):
        """
        """
        self.file_name = "account_balance.txt"
        # For efficiency, file read/write operations are minimized
        # by loading the whole csv to a list during this object's
        # construction so that we only need to interact with list
        # and only update the file when necessary.
        self.accounts = load_from_file(self.file_name)

    def account_login(self):
        """
        Handles all operations associated with the login process.
        """
        for i in range(3, 0, -1):
            phone_number = input("Phone number: ")
            row_dict = self.get_row(phone_number)

            if not row_dict:
                print(f"\nAccount not found. {i-1} attempts remaining\n")
                continue

            pin = input("PIN: ")

            hash = pin_hasher(row_dict["salt"], pin)

            if (hash == row_dict["pin_number"]):
                print("\nLogin successful. Welcome back.\n")
                print("\n--- Main Menu ---")
                transaction = Transaction()
                transaction.transact()
                return

            print(f"\nWrong PIN. {i-1} attempts remaining.\n")
        else:
            return

    def get_row(self, phone_num):
        """
        Returns a dictionary containing the given phone_number,
        otherwise returns empty dictionary.
        """
        for row in self.accounts:
            if (phone_num == row["phone_number"]):
                return row
        return {}
