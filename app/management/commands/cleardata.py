from typing import Any
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from app import models

class Command(BaseCommand):
    help = 'clear fake data'

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            user: User = User.objects.get(username='test_user')
        except User.DoesNotExist:
            self.stdout.write('Test user not found ' + self.style.WARNING('warning'))
        else:
            user.delete()
            self.stdout.write('Test user and data delete ' + self.style.SUCCESS('Ok'))

        models.Currency.objects.all().delete()
        self.stdout.write('Data delete ' + self.style.SUCCESS('Ok'))

