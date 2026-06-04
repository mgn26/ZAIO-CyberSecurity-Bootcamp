"""
This module implements the AccountBalance class used in PyBank ATM.
"""
from enum import Enum
from .account import Account


class TransactType(Enum):
    """
    This is an Enum class

    Enum - is a special data type used to define a set of named constants
    """
    WITHDRAW = 1
    DEPOSIT = 2
    EFT_IN = 3
    EFT_OUT = 4


class AccountTransact(Account):
    """
    Represents a user account with added balance attribute.

    Inherits from Account.

    Attributes:
        transact_type (TransactType): Store transaction type
        amount (float): Store Transaction amount
        balance (float): Store User's current account balance
    """

    def __init__(self, phone_num, acc_num, trans_type, amount, balance):
        """
        Inititalizes parent objects and local attributes.
        """
        super().__init__(phone_num, acc_num)
        self.transact_type = trans_type
        self.amount = amount
        self.balance = balance
