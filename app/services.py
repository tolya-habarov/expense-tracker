from django.db import models
from django.db import transaction

from app.models import Transaction, Account


@transaction.atomic
def add_transaction(transaction: Transaction) -> None:
    account = transaction.account
    if transaction.transaction_type == Transaction.Type.EXPENSE:
        account.current_balance -= transaction.amount
    elif transaction.transaction_type == Transaction.Type.INCOME:
        account.current_balance += transaction.amount

    transaction.save()
    account.save()


@transaction.atomic
def update_balance(account: Account) -> None:
    income = account.transactions.filter(transaction_type=Transaction.Type.INCOME)
    expence = account.transactions.filter(
        models.Q(transaction_type=Transaction.Type.EXPENSE) |
        models.Q(transaction_type=Transaction.Type.TRANSFER)
    )

    agg = lambda x: x.aggregate(models.Sum('amount')).get('amount__sum')

    if income:
        account.current_balance += agg(income)
    
    if expence:
        account.current_balance -= agg(expence)
    
    account.save()
