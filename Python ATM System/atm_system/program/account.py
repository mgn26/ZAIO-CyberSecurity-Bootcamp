"""
This module implements the account class used in PyBank ATM.
"""


class Account:
    """
    Represents a user account and it's operations.

    Attributes:
        phone_number (str): stores user account's phone number
        account_number (str): stores generated account number
        pin_number (str): stores hashed pin number
        salt (str): stores generated salt string
    """
    def __init__(self, phone_num, acc_num, pin_num, salt):
        self.phone_number = phone_num
        self.account_number = acc_num
        self.salt = salt
        self.pin_number = pin_num
