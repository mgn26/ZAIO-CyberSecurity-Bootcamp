"""
This module contains a hashing function to secure the pin number.
"""
import hashlib


def pin_hasher(salt, pin_num):
    """
    This function generates a hash for a given input.
    """
    digest = hashlib.sha256((str(salt) + str(pin_num)).encode()).hexdigest()
    return digest
