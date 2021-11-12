from django.contrib.auth.models import Permission
from django.db.models import query
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from datetime import datetime, timedelta

from django.db import transaction

from app.user.models import User
from app.accounts.models import AccountHistory, Account

from .serializers import AccountSerializer, AccountHistorySerializer
from .pagination import CustomPagination

class AccountViewset(UpdateModelMixin, GenericViewSet):
    quryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountSerializer

    def create(self, request, *args, **kwargs):
        request.data.setdefault('user', request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountHistoryViewset(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = AccountHistory.objects.all()
    serializer_class = AccountHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountHistorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data.setdefault('account', Account.objects.get(id=request.user.id).id)
        request.data.setdefault('transaction_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        word = self.request.query_params.get('kind', None)
        start_date = self.request.query_params.get('start_date', self.get_queryset().first().transaction_date)
        last_date = self.request.query_params.get('last_date', self.get_queryset().last().transaction_date + timedelta(days=1))
        if word:
            queryset = self.get_queryset().filter(kind=word, transaction_date__range=[start_date, last_date])
        else:
            queryset = self.get_queryset(transaction_date__range=[start_date, last_date])
        serializer = AccountHistorySerializer(queryset, many=True)
        return Response(serializer.data)
