"""
This module implements the account class used in PyBank ATM.
"""
from .timestamp_gen import timestamp_gen

# This class is a parent class.
class Account:
    """
    Represents the basic user account and it's basic operations.

    Attributes:
        timestamp (datetime): Stores an activity timestamp
        phone_number (str): stores user account's phone number
        account_number (str): stores generated account number
    """
    
    def __init__(self, phone_num, acc_num):
        """
        Initializes this object's state.
        """
        self.timestamp = timestamp_gen()
        self.phone_number = phone_num
        self.account_number = acc_num
        

    def to_dict(self):
        """
        Returns this object in it's dictionary form.
        """
        # This method is meant to be overwritten when needed. 
        return self.__dict__
