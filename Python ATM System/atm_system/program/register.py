"""
This module implement the register class used in PyBank ATM.
"""
from .account_balance import AccountBalance
from .str_gen import acc_num_gen, rand_str_gen
from .pin_hasher import pin_hasher
from .file_operation import *  # file_operation just contains a few functions


class Register:
    """
    This class handles all operations associated with account creation.

    Attributes:
        file_name (str):
        accounts (list):
    """
    def __init__(self):
        """
        Initializes this object's attributes.
        """
        self.file_name = "account_balances.txt"
        # For efficiency, file read/write operations are minimized
        # by loading the whole csv to a list during this object's
        # construction so that we only need to interact with list
        # and only update the file when necessary.
        self.accounts = load_from_file(self.file_name)

    def __del__(self):
        """
        Saves this object's state to file before destruction.
        """
        # To ensure that the csv file that was loaded to memory
        # during construction is up to date with this object's state.
        save_to_file(self.file_name, self.accounts)

    def create_account(self):
        """
        Handles all registration operations.
        """
        phone_num = self.get_phone_num()
        if (phone_num == 0):
            print("\nRegistration failed.")
            return

        pin = self.get_pin()
        if (pin == 0):
            print("\nRegistration failed.")
            return

        salt = rand_str_gen()
        hash = pin_hasher(salt, pin)

        # Prevent account number duplicates
        acc_num = acc_num_gen()
        while True:
            for row in self.accounts:
                if (acc_num in row):
                    break
            else:
                break
            acc_num = acc_num_gen()

        account = AccountBalance(phone_num, acc_num, hash, salt)

        self.accounts.append(account.to_dict())

        # System should work fine without the following line.
        # This is for 'just in case'.
        write_to_csv(self.file_name, account)

        print("\nRegistration Successful.")
        print(f"Your account number is: {account.account_number}")
        print("Please save this number."
              "You will need it to receive transfers.")

    def get_phone_num(self):
        """
        Gets a phone number from user input.
        """
        phone_number = input("Enter your phone number (10 digits): ")

        if (len(phone_number) != 10):
            print("\nPhone number must be exactly 10 digits long.")
            return 0
        elif (not phone_number.isdigit()):
            print("\nPhone number must contain only digits.")
            return 0
        elif (self.search_phone_number(phone_number)):
            print("\nPhone number already exists.")
            return 0
        else:
            return phone_number

    def get_pin(self):
        """
        Gets a pin and it's confirmation from user input.
        """
        pin_num = input("Create a PIN (4-5 digits): ")
        pin_num_confirm = input("Confirm PIN: ")

        if (pin_num != pin_num_confirm):
            print("\nPlease make sure the PINs match.")
            return 0

        if (len(pin_num) != 5 and len(pin_num) != 4):
            print("\nPIN must either be 4 or 5 digits long")
            return 0

        return pin_num

    def search_phone_number(self, phone_number):
        """
        Returns true if given phone_number is found, false otheriwise.
        """
        for row in self.accounts:
            if (phone_number == row["phone_number"]):
                return True
        return False
