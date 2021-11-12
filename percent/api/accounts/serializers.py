from django.db.models import fields
from django.http import request
from rest_framework import serializers
from rest_framework.validators import ValidationError

from app.accounts.models import Account, AccountHistory
from app.user.models import User
from api.user.serializers  import UserSerializer


class AccountSerializer(serializers.ModelSerializer):

    user = UserSerializer

    class Meta:
        model = Account
        fields = ['user', 'account_number', 'price']

    def create(self, validated_data):
        instance = Account.objects.create(**validated_data)
        return instance

class AccountHistorySerializer(serializers.ModelSerializer):

    account = AccountSerializer

    class Meta:
        model = AccountHistory
        fields = ['account', 'kind', 'transaction_date', 'amount', 'etc']

    def validate(self, value):
        if value['kind'] not in [AccountHistory.DEPOSIT, AccountHistory.WITHDRAW]:
            raise ValidationError
        return value

    def create(self, validated_data):

        if validated_data["kind"] == "deposit":
            validated_data['account'].price += validated_data['amount']
            validated_data['account'].save()
            

        if validated_data["kind"] == "withdraw":
            if validated_data['account'].price >= validated_data['amount']:
                validated_data['account'].price -= validated_data['amount']
                validated_data['account'].save()

            if validated_data['account'].price < validated_data['amount']:
                raise Exception("No balance")

        instance = AccountHistory.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):

        return {
            'account_id' : instance.account_id,
            '거래금액' : instance.amount,
            '잔액' : instance.account.price,
            '거래종류' : instance.kind,
            '적요' : instance.etc,
            '거래일자' : instance.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
        }