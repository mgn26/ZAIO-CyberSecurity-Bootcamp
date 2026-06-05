"""
This module implement the log class used in PyBank ATM.
"""

from .file_operation import *  # file_operation just contains a few functions
from .account_log import AccountLog, EventType


class Log:
    """
    This class handles all operations associated with
    logging all system activities.
    """

    def __init__(self):
        """
        Initializes this class's object.

        Attributes:
            log_file_name (str): The name of the log file.
            event_type (EventType): An Enum object of EventType.
        """
        self.log_file_name = "log.txt"
        self.event_types = EventType

    def to_log(self, phone_num, event_type):
        """
        Writes log data to file.
        """
        write_to_csv(self.log_file_name, AccountLog(phone_num, "", event_type))
