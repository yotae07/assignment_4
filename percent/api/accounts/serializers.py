from rest_framework import serializers
from app.accounts.models import Account, AccountHistory
from rest_framework.exceptions import ValidationError

class AccountHistorySerializer(serializers.ModelSerializer):


    class Meta:
        model = AccountHistory
        field = ['id', 'kind', 'transaction_data', 'amount', 'etc']

    def validate_kind(self, value):
        if value not in [AccountHistory.DEPOSIT, AccountHistory.WITHDRAW]:
            raise ValidationError
        
        return value

    def create(self, validated_data):
        instance = AccountHistory.objects.create()
        
        if validated_data['kind'] == AccountHistory.DEPOSIT:
            validated_data['account'].price += validated_data['amount']
            validated_data['account'].save()

        elif validated_data['kind'] == AccountHistory.WITHDRAW:
            if validated_data['account'].price > validated_data['amount']:
                validated_data['account'].price -= validated_data['amount']
                validated_data['account'].save()

            else:
                raise Exception("lower then price")

        return instance


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        field = ['id', 'user','account_number', 'price']

    def validate_price(self, value):
        if int(value) < 0:
            raise ValidationError('Price Error')
        return value

    