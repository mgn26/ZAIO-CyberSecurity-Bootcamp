"""
This module contains file operation functions.
"""
import os
import csv


def write_to_csv(file_name, object):
    """
    Writes the state of a given object to a csv file.
    """
    headers = object.to_dict().keys()
    file_exists = check_file_exists(file_name)

    open_mode = "w"
    if (file_exists):
        open_mode = "a"

    with open(file_name, open_mode, newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if (not file_exists):
            writer.writeheader()
        writer.writerow(object.to_dict())


def check_file_exists(file_name):
    """
    Returns true if given file exists, false otherwise
    """
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        return True
    else:
        return False


def load_from_file(file_name):
    """
    Returns a dictionary of all the data from the given file.
    """
    file_exists = check_file_exists(file_name)

    if (not file_exists):
        return []

    with open(file_name, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)


def save_to_file(file_name, list):
    """
    Saves everything from the given list to a given file.
    """
    if not list:
        return
    with open(file_name, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list[0].keys())
        writer.writeheader()
        writer.writerows(list)
