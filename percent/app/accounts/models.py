from django.db import models
from app.user.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    account_number = models.CharField(max_length=32, unique=True)
    price = models.PositiveBigIntegerField(default=0)


class AccountHistory(models.Model):
    DEPOSIT, WITHDRAW = ('deposit', 'withdraw')
    KIND_CHOICES = (
        (DEPOSIT, '입금'),
        (WITHDRAW, '출금')
    )

    kind = models.CharField(choices=KIND_CHOICES, max_length=10)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveBigIntegerField()
    etc = models.CharField(max_length=1000)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null = True, blank = True)
