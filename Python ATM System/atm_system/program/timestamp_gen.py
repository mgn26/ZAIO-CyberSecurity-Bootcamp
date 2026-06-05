"""
This module contains the timestamp generator function.
"""
from datetime import datetime


def timestamp_gen():
    """
    Returns a timestamp.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp
