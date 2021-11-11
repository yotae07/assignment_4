from rest_framework import serializers
from app.user.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        field = ['id', 'name']
        exclude = ['password']

    def validate(self, attrs):
        attrs['password'] = attrs['name']
        return attrs

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance
