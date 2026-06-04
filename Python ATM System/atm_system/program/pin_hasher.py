"""
This module contains a hashing function to secure the pin number.
"""
import hashlib


def pin_hasher(salt, pin_num):
    """
    This function generates a hash for a given input.
    """
    string = str(salt) + str(pin_num)
    # SHA-256 used as its widely trusted and used in production systems.
    digest = hashlib.sha256(string).encode("utf-8").hexdigest()
    return digest
