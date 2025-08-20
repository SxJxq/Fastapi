#the name of the test file is important, it have to start with test word, even the function 
#WE DONT NEED THIS FILE

from app.calculations import add, BankAccount, InsufficiantFunds
import pytest

@pytest.fixture #to handle repetitave code, it runs before the test
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,1,8),
    (12,4,16)
])


def test_add(num1,num2,expected):
    print("testing")
    assert add(num1,num2) == expected

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance==30

def test_deposit(bank_account):
   bank_account.deposit(20)
   assert bank_account.balance==70

def test_collect_interest(bank_account):
   bank_account.collect_interest()
   assert round(bank_account.balance,6)==55



@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100,100),
    (50,10,40),
    (1200,200,1000)
    
    
])


def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_no_enough_mony(bank_account):
    with pytest.raises(InsufficiantFunds):
        bank_account.withdraw(200)

