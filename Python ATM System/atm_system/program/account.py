"""
This module implements the account class used in PyBank ATM.
"""

class Account:
    """
    Represents a user account and it's operations.

    Attributes:
    """

    def __init__(self, phone_num, pin_num):
        #store a hash of the pin
        #self.pin_num = pin_num
        #used as username
        self.phone_num = phone_num
        #auto generate account number
        #self.acc_num = acc_num
