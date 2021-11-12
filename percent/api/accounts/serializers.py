from rest_framework import serializers
from app.accounts.models import AccountHistory
from rest_framework.exceptions import ValidationError

class AccountInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountHistory
        fields =['kind', 'transaction_date', 'amount', 'etc', 'account.price' ]

    def validate(self, attrs):
        return attrs


    def to_representation(self, instance):
        return {
            'transaction_type': instance.kind,
            'transaction_date': instance.transaction_date,
            'transaction_amount': instance.amount,
            'transaction_etc': instance.etc,
            'transaction_balance': instance.account.price
        }