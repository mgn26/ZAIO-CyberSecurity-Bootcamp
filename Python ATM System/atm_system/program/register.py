"""
This module implement the register class used in PyBank ATM.
"""
from .str_gen import acc_num_gen, rand_str_gen
from .pin_hasher import pin_hasher


class Register:
    """
    This class handles all operations associated with account creation.
    """
    def __init__(self):
        self.phone_number = None
        self.acc_num = None
        self.salt = None
        self.pin = None

    def create_account(self):
        self.phone_number = self.get_phone_num();
        if (self.phone_number == 0):
            print("\nRegistration failed.")
            return
        
        self.pin = self.get_pin()
        
        if (self.pin == 0):
            print("\nRegistration failed.")
            return

        self.salt = rand_str_gen()
        self.pin = pin_hasher(self.salt, self.pin)
        
        self.acc_num = acc_num_gen()
        print("\nRegistration Successful.")
        print(f"Your account number is: {self.acc_num}")
        print("Please save this number. You will need it to receive transfers.") 

    def get_phone_num(self):
        phone_number = input("Enter your phone number (10 digits): ")

        if (len(phone_number) != 10):
            print("\nPhone number must be exactly 10 digits long.")
            return 0
        elif (not phone_number.isdigit()):
            print("\nPhone number must contain only digits.")
            return 0
        else:
            return phone_number

    def get_pin(self):
        pin_num = input("Create a PIN (4-5 digits): ")
        pin_num_confirm = input("Confirm PIN: ")

        if (pin_num != pin_num_confirm):
            print("\nPlease make sure the PINs match.")
            return 0

        if (len(pin_num) != 5 and len(pin_num) != 4):
            print("\nPIN must either be 4 or 5 digits long")
            return 0

