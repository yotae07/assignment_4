from rest_framework import serializers
from app.accounts.models import Account, AccountHistory
from rest_framework.exceptions import ValidationError

from api.user.serializers import UserSerializer

class AccountSerializer(serializers.ModelSerializer):
    user           = UserSerializer(required=False)
    account_number = serializers.CharField(max_length=32, required=False)
    price          = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['user','account_number', 'price']

    def get_price(self, obj):
        return abs(obj.price)

    def validate_price(self, value):
        if int(value) < 0:
            raise ValidationError('Price Error')
        return value

    def create(self, validated_data):
        instance = Account.objects.create(**validated_data)

        return instance

    def to_representation(self, instance):
        return {
            'id'             : instance.id,
            'user'           : UserSerializer.data,
            'account_number' : instance.account_number,
            'price'          : instance.price,
        }

class AccountHistorySerializer(serializers.ModelSerializer):
    
    account = AccountSerializer(required=False)
    kind    = serializers.CharField(max_length=10)
    etc     = serializers.CharField(max_length=1000)
    amount  = serializers.SerializerMethodField()

    class Meta:
        model = AccountHistory
        fields = ['kind', 'account','transaction_data', 'amount', 'etc']

    def get_price(self, obj):
        return abs(obj.amount)

    def validate_kind(self, value):
        if value not in [AccountHistory.DEPOSIT, AccountHistory.WITHDRAW]:
            raise ValidationError("wrong kind type")
        
        return value

    def create(self, validated_data):
        instance = AccountHistory.objects.create(**validated_data)
        
        if validated_data['kind'] == AccountHistory.DEPOSIT:
            validated_data['account'].price += validated_data['amount']
            validated_data['account'].save()

        elif validated_data['kind'] == AccountHistory.WITHDRAW:
            if validated_data['account'].price > validated_data['amount']:
                validated_data['account'].price -= validated_data['amount']
                validated_data['account'].save()

            else:
                raise ValidationError("lower then price")

        return instance
    