"""
This module implement the transactions class used in PyBank ATM.
"""

from .file_operation import *  # file_operation just contains a few functions
from .account_transact import AccountTransact, TransactType
from .log import Log


class Transaction:
    """
    This class handles all operations associated with performing transactions.

    Attributes:
        acc_bal_file (str): Name of account_balance file.
        transact_file (str): Name of transactions file.
        account_balances (list): List of dictionaries which represent
            account_balance rows.
        transactions (list): List of dictionaries which represent
            transactions.
        active_account (dict): Row of the logged in account.
        recipient_account (dict): Row of the recipient account.
        sys_log (Log): An object of the Log class.
    """

    def __init__(self, accounts, active_acc):
        """
        Initializes Transaction object.
        """
        # This object will need to update file contents for both files.
        self.acc_bal_file = "account_balances.txt"
        self.transact_file = "transactions.txt"

        # Little more efficient passing accounts at the cost of robustness.
        self.accounts_balances = accounts
        self.transactions = load_from_file(self.transact_file)
        self.active_account = active_acc
        self.recipient_account = None
        self.sys_log = Log()

    def __del__(self):
        """
        Saves this object's state to file before destruction.
        """
        # To ensure that the csv file that was loaded to memory
        # during construction is up to date with this object's state.
        save_to_file(self.acc_bal_file, self.accounts_balances)
        save_to_file(self.transact_file, self.transactions)

    def transact(self):
        """
        Handles all transactional processes of the system.
        """
        while True:
            print(self.main_menu())
            option = int(input("Select an option: "))
            if option == 1:
                print("\n--- Withdraw ---")
                self.withdraw()
            elif option == 2:
                print("\n--- Deposit ---")
                self.deposit()
            elif option == 3:
                print("\n--- EFT Transfer ---")
                self.transfer()
            elif option == 4:
                print("\n--- Statement ---")
                self.view_statement()
            elif option == 5:
                print("\nLogged out. Stay safe.")
                self.sys_log.to_log(
                    self.active_account["phone_number"],
                    self.sys_log.event_types.USER_LOGOUT.name,
                )
                break
            else:
                print("\nPlease choose a valid option.")

    def withdraw(self):
        """
        Subtracts a specified amount from balance.
        """
        input_amount = float(input("\nAmount to Withdraw: R "))
        curr_balance = float(self.active_account["balance"])

        if curr_balance < input_amount:
            print("\nInsufficient Funds.")
            self.sys_log.to_log(
                self.active_account["phone_number"],
                self.sys_log.event_types.WITHDRAWAL_FAILED.name,
            )
            return

        curr_balance -= input_amount
        self.active_account["balance"] = curr_balance

        account_transact = AccountTransact(
            self.active_account["phone_number"],
            self.active_account["account_number"],
            TransactType.WITHDRAW.name,
            input_amount,
            curr_balance,
        )

        self.transactions.append(account_transact.to_dict())

        save_to_file(self.transact_file, self.transactions)
        save_to_file(self.acc_bal_file, self.accounts_balances)

        print(f"\nWithdrawal successful. New balance: R{curr_balance:.2f}")
        self.sys_log.to_log(
            self.active_account["phone_number"],
            self.sys_log.event_types.WITHDRAWAL_SUCCESSFUL.name,
        )

    def deposit(self):
        """
        Adds a specified amount to balance.
        """
        input_amount = float(input("\nAmount to Deposit: R "))
        curr_balance = float(self.active_account["balance"])

        if input_amount <= 0:
            print("\nInvalid amount.")
            self.sys_log.to_log(
                self.active_account["phone_number"],
                self.sys_log.event_types.DEPOSIT_FAILED.name,
            )
            return

        curr_balance += input_amount
        self.active_account["balance"] = curr_balance

        account_transact = AccountTransact(
            self.active_account["phone_number"],
            self.active_account["account_number"],
            TransactType.DEPOSIT.name,
            input_amount,
            curr_balance,
        )

        self.transactions.append(account_transact.to_dict())

        save_to_file(self.transact_file, self.transactions)
        save_to_file(self.acc_bal_file, self.accounts_balances)

        print(f"\nDeposit successful. New balance: R{curr_balance:.2f}")
        self.sys_log.to_log(
            self.active_account["phone_number"],
            self.sys_log.event_types.DEPOSIT_SUCCESSFUL.name,
        )

    def transfer(self):
        """
        Performs the transfer operation between two accounts.
        """
        # There could have been a loop here to mimic
        # the exact behaviour from the spec, but this
        # approach makes more sense to me and not following
        # the spec here is not a train smash.
        if not self.get_acc_num():
            self.sys_log.to_log(
                self.active_account["phone_number"],
                self.sys_log.event_types.TRANSFER_FAILED.name,
            )
            return

        input_amount = float(input("Amount to transfer: R "))
        curr_balance = float(self.active_account["balance"])

        if curr_balance < input_amount:
            print("\nInsufficient Funds.")
            self.sys_log.to_log(
                self.active_account["phone_number"],
                self.sys_log.event_types.TRANSFER_FAILED.name,
            )
            return

        rec_balance = float(self.recipient_account["balance"])

        curr_balance -= input_amount
        rec_balance += input_amount

        self.active_account["balance"] = curr_balance
        self.recipient_account["balance"] = rec_balance

        account_transact = AccountTransact(
            self.active_account["phone_number"],
            self.active_account["account_number"],
            TransactType.EFT_OUT.name,
            input_amount,
            curr_balance,
        )

        self.transactions.append(account_transact.to_dict())

        save_to_file(self.transact_file, self.transactions)
        save_to_file(self.acc_bal_file, self.accounts_balances)

        print(
            f"\nTransfer successful. R{input_amount:.2f} sent to "
            f"account {self.recipient_account["account_number"]}."
        )
        print(f"Your new balance: R{curr_balance:.2f}")
        self.sys_log.to_log(
            self.active_account["phone_number"],
            self.sys_log.event_types.TRANSFER_SUCCESSFUL.name,
        )

    def view_statement(self):
        """
        Prints the logged in user's transactions.
        """
        for row in self.transactions:
            if row["phone_number"] == self.active_account["phone_number"]:
                print(
                    f"{row["timestamp"]} | "
                    f"{row["transact_type"]} | "
                    f"{self.get_sign(row["transact_type"])}"
                    f"R{float(row["amount"]):.2f} | "
                    f"Balance: R{float(row["balance"]):.2f}"
                )

    def get_sign(self, transact_type):
        """
        Determines the sign to print on statement.
        """
        if transact_type in \
           [TransactType.EFT_OUT.name, TransactType.WITHDRAW.name]:
            return "-"
        else:
            return "+"

    def main_menu(self):
        """
        Displays menu to terminal.
        """
        main_menu = (
            "\n--- Main Menu ---\n"
            "1. Withdraw\n"
            "2. Deposit\n"
            "3. Transfer (EFT)\n"
            "4. View Statement\n"
            "5. Logout\n"
        )
        return main_menu

    def get_acc_num(self):
        """
        Gets account number from user input and validates it.
        """
        acc_num = input("\nEnter recipient account number (8 digits): ")

        if len(acc_num) != 8:
            print("\nAccount number must be 8 digits long.")
            return False

        if acc_num == self.active_account["account_number"]:
            print("\nYou cannot make a transfer to yourself.")
            return False

        for row in self.accounts_balances:
            if acc_num == row["account_number"]:
                self.recipient_account = row
                return True
        else:
            print(
                "\nError: Account not found. "
                "Please check the account number and try again."
            )

        return False
