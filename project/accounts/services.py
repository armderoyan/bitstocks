from .models import Account, Transaction
from django.db import transaction as trans
from decimal import Decimal

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@trans.atomic
def perform_deposit(user, amount):
    # This code executes inside a transaction.

    if amount <= 0:
        raise Exception('Invalid amount')

    try:
        # will lock rows until the end of the transaction
        account = Account.objects.select_for_update().get(user=user)
    except Account.DoesNotExist:
        logger.error('Invalid Account: ' + str(user))
        return

    try:
        account.balance = decimal_increase(account.balance, amount)
        account.save()

        transaction = Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TRANSACTION_TYPE_DEPOSIT
        )

        return transaction
    except:
        # log some message
        logger.error('Transaction failed. User : ' + str(user) + ', Transaction Amount :' + str(amount))
        return


@trans.atomic
def perform_withdrawal(user, amount):
    # This code executes inside a transaction.

    if amount <= 0:
        raise Exception('Invalid amount')

    try:
        # will lock rows until the end of the transaction
        account = Account.objects.select_for_update().get(user=user)
    except Account.DoesNotExist:
        logger.error('Invalid User: ' + str(user))
        return

    try:
        if account.balance >= amount:
            account.balance = decimal_reduce(account.balance, amount)
            account.save()

            transaction = Transaction.objects.create(
                account=account,
                transaction_type=Transaction.TRANSACTION_TYPE_WITHDRAWAL
            )

            return transaction

        raise Exception('There is not enough balance in your account')
    except:
        # log some message
        logger.error('Transaction failed. User : ' + str(user) + ', Transaction Amount :' + str(amount))

        return


def decimal_increase(value1, value2):
    return float(Decimal(str(value1)) + Decimal(str(value2)))


def decimal_reduce(value1, value2):
    return float(Decimal(str(value1)) - Decimal(str(value2)))
