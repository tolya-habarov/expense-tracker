import random
from pytz import UTC
import datetime as dt
from typing import Any
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app import models

CURRENCIES = [
    {'name': 'U.S. Dollar', 'symbol': 'USD'},
    {'name': 'European Euro', 'symbol': 'EUR'},
    {'name': 'Japanese Yen', 'symbol': 'JPY'},
    {'name': 'British Pound', 'symbol': 'GBP'},
    {'name': 'Russian ruble', 'symbol': 'RUB'},
]

ACCOUNTS = ['Cash', 'Card']

CATEGORIES = [
    'Housing',
    'Transportation',
    'Food',
    'Utilities',
    'Insurance',
    'Medical',
    'Clothing',
    'Education',
]

PAYEES = [
    'Walmart',
    'McDonald’s',
    'Subway',
    'Starbucks',
    'Walgreens',
    'Target',
    'Taco Bell',
    'Burger King',
]

_currend_date = dt.datetime.today().replace(day=1, tzinfo=UTC)
FIRST_DATE = _currend_date.replace(month=_currend_date.month - 1)
SECOND_DATE = _currend_date
END_DATE = _currend_date.replace(month=_currend_date.month + 1)

NOTES = 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Aliquam magni accusantium maiores praesentium, placeat possimus est tenetur quos iste deserunt nulla soluta, iusto inventore vel minima adipisci exercitationem accusamus eius?'


class Command(BaseCommand):
    help = 'create fake data'

    @staticmethod
    def random_date(start: dt.datetime, end: dt.datetime) -> dt.datetime:
        between_dates = end - start
        days_delta = random.randrange(between_dates.days)
        return start + dt.timedelta(days=days_delta)

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            user: User = User.objects.get(username='test_user')
            self.stdout.write('Test user found ' + self.style.SUCCESS('Ok'))
        except User.DoesNotExist:
            user = User(username='test_user', email='test_user@mail.com')
            user.set_password('1234test')
            user.save()
            self.stdout.write('Test user created ' + self.style.SUCCESS('Ok'))

        self.stdout.write(self.style.NOTICE('Creating fake data:'))

        currencies = [models.Currency(id=i, **x) for i, x in enumerate(CURRENCIES)]
        models.Currency.objects.bulk_create(currencies)
        self.stdout.write('Create currencies ' + self.style.SUCCESS('Ok'))

        new_account = lambda id, name: models.Account(
            id=id,
            name=name,
            user=user,
            currency=random.choice(currencies),
            balance=Decimal(random.randrange(10) * 10000),
        )
        accounts = [new_account(id, name) for id, name in enumerate(ACCOUNTS)]
        models.Account.objects.bulk_create(accounts)
        self.stdout.write('Create accounts ' + self.style.SUCCESS('Ok'))

        categories = [models.Category(i, name, user=user) for i, name in enumerate(CATEGORIES)]
        models.Category.objects.bulk_create(categories)
        self.stdout.write('Create categories ' + self.style.SUCCESS('Ok'))

        payees = [models.Payee(i, name, user=user) for i, name in enumerate(PAYEES)]
        models.Payee.objects.bulk_create(payees)
        self.stdout.write('Create payees ' + self.style.SUCCESS('Ok'))

        transactions, count = [], 15
        for i in range(count):
            if i < count / 2:
                date = self.random_date(FIRST_DATE, SECOND_DATE)
            else:
                date = self.random_date(SECOND_DATE, END_DATE)

            transactions.append(
                models.Transaction(
                    id=i,
                    name=f'Transaction{i+1}',
                    date=date,
                    notes=NOTES,
                    amount=Decimal('.00'),
                    account=random.choice(accounts),
                    transaction_type=random.choice(models.Transaction.Type.values),
                    category=random.choice(categories),
                    payee=random.choice(payees),
                )
            )
        transactions = models.Transaction.objects.bulk_create(transactions)
        self.stdout.write('Create transactions ' + self.style.SUCCESS('Ok'))
