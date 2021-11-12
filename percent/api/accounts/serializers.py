from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import ValidationError

from app.accounts.models import Account, AccountHistory

class TransactionSerializer(serializers.ModelSerializer):
    account_number   = serializers.CharField(max_length=32)
    kind             = serializers.CharField(max_length=10)
    amount           = serializers.IntegerField()
    etc              = serializers.CharField(max_length=1000)

    class Meta:
        model = AccountHistory
        fields = ['id', 'account_number', 'account_id', 'kind', 'amount', 'etc']

    def validate_kind(self, value):
        if value not in [AccountHistory.DEPOSIT, AccountHistory.WITHDRAW]:
            raise ValidationError("value Error")
    
        return value
    
    def create(self, validated_data):
        account_number = validated_data['account_number']
        kind           = validated_data['kind']
        amount         = validated_data['amount']
        etc            = validated_data['etc']
        user_id = self.context['request'].user.id
        account = Account.objects.get(user_id = user_id)

        if not Account.objects.get(user_id = user_id).exists():
            raise ValidationError("No Account")

        if amount < 0:
            raise ValidationError('wrong request')

        if kind == "withdraw" and int(amount) > int(account.price):
            raise ValidationError('wrong request')

        if Account.objects.get(user_id = user_id).account_number != account_number:
            raise ValidationError('Incorrect account_number')
        
        with transaction.atomic():
            history = AccountHistory.objects.create(kind = kind, amount = amount, etc = etc, account = account)
            
            if kind == 'deposit':
                account.price += amount
                account.save()
            elif kind == 'withdraw':
                account.price -= amount
                account.save()

        return history

    def to_representation(self, instance):
        return {
            'id'               : instance.id,
            'account_id'       : instance.account_id,
            'kind'             : instance.kind,
            'transaction_date' : instance.transaction_date,
            'amount'           : instance.amount,
            'etc'              : instance.etc
        }
