from django.db import models
from django.db import transaction

from app.models import Transaction, Account


@transaction.atomic
def add_transaction(transaction: Transaction) -> None:
    account = transaction.account
    if transaction.transaction_type == Transaction.Type.EXPENSE:
        account.balance = account.balance - transaction.amount
    elif transaction.transaction_type == Transaction.Type.INCOME:
        account.balance = account.balance + transaction.amount

    transaction.save()
    account.save()


@transaction.atomic
def update_balance(account: Account) -> None:
    income = account.transactions.filter(transaction_type=Transaction.Type.INCOME)
    expence = account.transactions.filter(
        models.Q(transaction_type=Transaction.Type.EXPENSE) |
        models.Q(transaction_type=Transaction.Type.TRANSFER)
    )
    income_amount = income.aggregate(models.Sum('amount')).get('amount__sum')
    expence_amount = expence.aggregate(models.Sum('amount')).get('amount__sum')
    account.balance = income_amount - expence_amount
    account.save()
