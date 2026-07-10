# bank.py

# ============================
# Optional Custom Exception
# ============================
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance."""
    pass


# ============================
# Task 1: Base Class
# ============================
class BankAccount:
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if amount > self.balance:
            # Raise custom exception if Task 3 is enabled
            raise InsufficientFundsError(
                f"Insufficient funds: cannot withdraw ${amount} from account {self.account_number}"
            )

        self.balance -= amount
        return self.balance

    def __str__(self):
        return f"Account {self.account_number} – Owner: {self.owner}, Balance: ${self.balance}"


# ============================
# Task 2: Subclass (SavingsAccount)
# ============================
class SavingsAccount(BankAccount):
    def __init__(self, account_number, owner, interest_rate, balance=0):
        super().__init__(account_number, owner, balance)
        self.interest_rate = interest_rate  # percent

    def apply_interest(self):
        interest_amount = self.balance * (self.interest_rate / 100)
        self.balance += interest_amount
        return self.balance

    def __str__(self):
        return (
            f"Savings Account {self.account_number} – Owner: {self.owner}, "
            f"Balance: ${self.balance}, Interest Rate: {self.interest_rate}%"
        )


# ============================
# Test Code
# ============================
if __name__ == "__main__":
    print("=== Task 1: BankAccount Tests ===")
    acct = BankAccount("12345", "Alice", 500)
    print(acct)

    # Successful deposit
    acct.deposit(200)
    print("After deposit:", acct)

    # Successful withdrawal
    acct.withdraw(100)
    print("After withdrawal:", acct)

    # Trigger insufficient funds
    try:
        acct.withdraw(1000)
    except InsufficientFundsError as e:
        print("Error:", e)

    print("\n=== Task 2: SavingsAccount Tests ===")
    sav = SavingsAccount("98765", "Bob", interest_rate=5, balance=1000)
    print(sav)

    # Inherited deposit
    sav.deposit(500)
    print("After deposit:", sav)

    # Inherited withdrawal
    sav.withdraw(200)
    print("After withdrawal:", sav)

    # Apply interest
    sav.apply_interest()
    print("After applying interest:", sav)


