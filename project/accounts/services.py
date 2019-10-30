from .models import Account, Transaction
from django.db import transaction as trans
from decimal import Decimal

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@trans.atomic
def perform_deposit(user, amount):
    # This code executes inside a transaction.

    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        logger.error('Invalid Account: ' + str(user))
        return

    try:
        sid = trans.savepoint()

        account.balance = decimal_increase(account.balance, amount)
        account.save()

        transaction = Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TRANSACTION_TYPE_DEPOSIT
        )

        trans.savepoint_commit(sid)
        return transaction
    except:
        # log some message
        logger.error('Transaction failed. User : ' + str(user) + ', Transaction Amount :' + str(amount))
        trans.savepoint_rollback(sid)
        return


@trans.atomic
def perform_withdrawal(user, amount):
    # This code executes inside a transaction.

    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        logger.error('Invalid User: ' + str(user))
        return

    try:
        if account.balance > amount:
            sid = trans.savepoint()
            account.balance = decimal_reduce(account.balance, amount)
            account.save()

            transaction = Transaction.objects.create(
                account=account,
                transaction_type=Transaction.TRANSACTION_TYPE_WITHDRAWAL
            )

            trans.savepoint_commit(sid)
            return transaction

        raise Exception('There is not enough balance in your account')
    except:
        # log some message
        logger.error('Transaction failed. User : ' + str(user) + ', Transaction Amount :' + str(amount))

        trans.savepoint_rollback(sid)
        return


def decimal_increase(value1, value2):
    return float(Decimal(str(value1)) + Decimal(str(value2)))


def decimal_reduce(value1, value2):
    return float(Decimal(str(value1)) + Decimal(str(value2)))
