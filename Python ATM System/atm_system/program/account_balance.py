"""
This module implements the AccountBalance class used in PyBank ATM.
"""
from .account import Account


class AccountBalance(Account):
    """
    Represents a user account with added balance attribute.

    Inherits from Account.

    Attributes:
        current_balance (float): User's account balance
    """

    def __init__(self, phone_num, acc_num, pin, salt, current_balance=0.0):
        """
        Inititalizes parent objects and local attributes.
        """
        super().__init__(phone_num, acc_num, pin, salt)
        self.current_balance = current_balance
