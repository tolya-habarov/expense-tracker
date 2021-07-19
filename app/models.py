from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class StrMixin():
    def __str__(self) -> str:
        return self.name # type: ignore

class Currency(StrMixin, models.Model):
    """Account currency"""

    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10)

    def __repr__(self) -> str:
        return self.name


class Account(StrMixin, models.Model):
    """Storage of transactions. For example card or cash"""

    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='accounts',
    )
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class Category(StrMixin, models.Model):
    """Transaction category"""

    name = models.CharField(max_length=50, unique=True)


class Payee(StrMixin, models.Model):
    """Payment receiver"""

    name = models.CharField(max_length=50, unique=True)


class Transaction(StrMixin, models.Model):
    """Account transaction"""

    class Type(models.TextChoices):
        EXPENSE = 'EP', _('EXPENSE')
        INCOME = 'IC', _('INCOME')
        TRANSFER = 'TF', _('TRANSFER')

    name = models.CharField(max_length=100, db_index=True)
    datetime = models.DateTimeField()
    notes = models.TextField(blank=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    transaction_type = models.CharField(
        max_length=2,
        choices=Type.choices,
        default=Type.EXPENSE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    payee = models.ForeignKey(
        Payee,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
