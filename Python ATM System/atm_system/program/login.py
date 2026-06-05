"""
This module implement the login class used in PyBank ATM.
"""

from .transaction import Transaction
from .log import Log
from .str_gen import acc_num_gen, rand_str_gen
from .pin_hasher import pin_hasher
from .file_operation import *  # file_operation just contains a few functions


class Login:
    """
    This class handles all operations associated with account management.
    """

    def __init__(self):
        """
        Initializes the Login object.

        Attributes:
            file_name (str): Account_balances file name.
            accounts (list): List of dictionaries that represent
                account_balances rows.
            active_account (dict): Dictionary of the current logged in account.
            sys_log (Log): Object of the Log class.
        """

        self.file_name = "account_balances.txt"
        # For efficiency, file read/write operations are minimized
        # by loading the whole csv to a list during this object's
        # construction so that we only need to interact with list
        # and only update the file when necessary.
        self.accounts = load_from_file(self.file_name)
        self.active_account = None
        self.sys_log = Log()

    def account_login(self):
        """
        Handles all operations associated with the login process.
        """
        for i in range(3, 0, -1):
            phone_number = input("Phone number: ")
            self.active_account = self.get_row(phone_number)

            if not self.active_account:
                print(f"\nAccount not found. {i-1} attempts remaining\n")
                self.sys_log.to_log(
                    phone_number, self.sys_log.event_types.LOGIN_FAILED.name
                )
                continue

            pin = input("PIN: ")

            hash = pin_hasher(self.active_account["salt"], pin)

            if hash == self.active_account["pin_number"]:
                print("\nLogin successful. Welcome back.\n")
                self.sys_log.to_log(
                    phone_number,
                    self.sys_log.event_types.LOGIN_SUCCESSFUL.name
                )
                transaction = Transaction(self.accounts, self.active_account)
                transaction.transact()
                return

            print(f"\nWrong PIN. {i-1} attempts remaining.\n")
            self.sys_log.to_log(
                phone_number, self.sys_log.event_types.LOGIN_FAILED.name
            )
        else:
            return

    def get_row(self, phone_num):
        """
        Returns a dictionary containing the given phone_number,
        otherwise returns empty dictionary.
        """
        for row in self.accounts:
            if phone_num == row["phone_number"]:
                return row
        return {}
