from django.test import TestCase
from django.contrib.auth.models import User

from .models import Account, Transaction
from .services import perform_deposit, perform_withdrawal


class DepositTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test@example.com')
        Account.objects.create(user=self.user, balance=0)

    def test_single_deposit(self):
        # Get the account and check 0 balance
        account = Account.objects.get(user=self.user)
        self.assertEquals(account.balance, 0)
        # Check 0 transactions in database
        self.assertEquals(Transaction.objects.count(), 0)

        # deposit 0.1 bitcoin
        perform_deposit(self.user, 0.1)

        # Check for 1 transaction in database
        self.assertEquals(Transaction.objects.count(), 1)
        # Check balance is now 0.1
        account = Account.objects.get(user=self.user)
        self.assertEquals(account.balance, 0.1)

    def test_multiple_deposit(self):
        # Get the account and check 0 balance
        account = Account.objects.get(user=self.user)
        self.assertEquals(account.balance, 0)
        # Check 0 transactions in database
        self.assertEquals(Transaction.objects.count(), 0)

        # deposit 0.1 bitcoin, 3 times
        perform_deposit(self.user, 0.1)
        perform_deposit(self.user, 0.1)
        perform_deposit(self.user, 0.1)

        # Check for 1 transaction in database
        self.assertEquals(Transaction.objects.count(), 3)
        # Check balance is now 0.1
        account = Account.objects.get(user=self.user)
        print(account.balance)

        self.assertEquals(account.balance, 0.3)

    def test_single_withdraw(self):
        # Get the account and check 0 balance
        account = Account.objects.get(user=self.user)
        self.assertEquals(account.balance, 0)

        # Check 0 transactions in database
        self.assertEquals(Transaction.objects.count(), 0)

        # deposit 0.1 bitcoin, 1 times
        perform_deposit(self.user, 0.1)
        perform_deposit(self.user, 0.1)

        # withdraw 0.1 bitcoin
        perform_withdrawal(self.user, 0.1)

        # Check for 1 transaction in database
        self.assertEquals(Transaction.objects.count(), 3)
        # Check balance is now 0.1
        account = Account.objects.get(user=self.user)
        self.assertEquals(account.balance, 0.1)

    def test_multiple_withdraw(self):
        # Get the account and check 0 balance
        account = Account.objects.get(user=self.user)
        self.assertEquals(account.balance, 0)
        # Check 0 transactions in database
        self.assertEquals(Transaction.objects.count(), 0)

        # deposit 0.3 bitcoin, 1 time
        perform_deposit(self.user, 0.2)

        # withdraw 0.1 bitcoin, 3 times
        perform_withdrawal(self.user, 0.1)
        perform_withdrawal(self.user, 0.1)
        perform_withdrawal(self.user, 0.1)

        # Check for 1 transaction in database
        self.assertEquals(Transaction.objects.count(), 3)
        # Check balance is now 0
        account = Account.objects.get(user=self.user)
        self.assertEquals(account.balance, 0)
