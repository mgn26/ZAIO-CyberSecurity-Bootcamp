"""
This module contains the account number and random string generator functions.
"""
import random
import string


def acc_num_gen(str_length=8):
    """
    This function simply generates a random set of numbers.
    """
    digits = random.choices(string.digits, k=str_length)
    result = "".join(digits)
    return result

def rand_str_gen(str_length=8):
    """
    This function simply generates a random string.
    """
    random_string = random.choices(string.ascii_letters + string.digits, k=str_length)
    result = "".join(random_string)
    return result
