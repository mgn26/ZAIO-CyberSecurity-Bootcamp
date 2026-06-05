"""
This module implements the AccountBalance class used in PyBank ATM.
"""
from enum import Enum
from .account import Account


class EventType(Enum):
    """
    This is an Enum class

    Enum - is a special data type used to define a set of named constants
    """

    LOGIN_SUCCESSFUL = 1
    LOGIN_FAILED = 2
    REGISTRATION_SUCCESSFUL = 3
    REGISTRATION_FAILED = 4
    WITHDRAWAL_SUCCESSFUL = 5
    WITHDRAWAL_FAILED = 6
    DEPOSIT_SUCCESSFUL = 7
    DEPOSIT_FAILED = 8
    TRANSFER_SUCCESSFUL = 9
    TRANSFER_FAILED = 10
    USER_LOGOUT = 11


class AccountLog(Account):
    """
    Represents a user account with added balance attribute.

    Inherits from Account.

    Attributes:
        event_type (EventType): Store event type.
    """

    def __init__(self, phone_num, acc_num, event_type):
        """
        Inititalizes parent objects and local attributes.
        """
        super().__init__(phone_num, acc_num)
        self.event_type = event_type

    def to_dict(self):
        """
        Returns the modified dictionary form of this object.
        """
        new_dict = self.__dict__
        new_dict.pop("account_number", None)
        return new_dict
