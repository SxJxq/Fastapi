def add(num1: int, nume2: int):
    return num1+nume2

class InsufficiantFunds(Exception):
    pass



class BankAccount():
    def __init__(self, starting_balance=0):#initial values, You use self to set attributes on the object
        self.balance=starting_balance

    def deposit(self, amount):
        self.balance+=amount

    def withdraw(self,amount):
        if amount>self.balance:
            raise InsufficiantFunds("no enough mony")
        self.balance-=amount

    def collect_interest(self):
        self.balance*=1.1