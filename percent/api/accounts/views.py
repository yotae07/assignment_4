from django.db.models import Q

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.validators import ValidationError

from app.accounts.models import Account, AccountHistory
from app.user.models import User
from .serializers import TransactionSerializer

from datetime import datetime, timedelta

class TransactionViewSet(CreateModelMixin, 
                         ListModelMixin, 
                         RetrieveModelMixin, 
                         UpdateModelMixin, 
                         DestroyModelMixin, 
                         GenericViewSet):
    queryset = AccountHistory.objects.all()
    serializer_class = TransactionSerializer
    permission_class = IsAuthenticated

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrive']:
            self.permission_class = permissions.IsAuthenticated

        return super().get_permissions()

    def creat(self, request, *arg, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def get_queryset(self):
        period = self.request.query_params.get('period', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        kind = self.request.query_params.get('kind', None)
        
        date = datetime.today()
        lists = AccountHistory.objects.all()

        if period:
            if period not in ["0", "1", "3", "7", "30", "90"]:
                raise ValidationError('wrong request')

        if period == "1":
            lists = AccountHistory.objects.filter(transaction_date__day = f"{date.day-1}")
        if period == "0":
            lists = AccountHistory.objects.filter(transaction_date__day = f"{date.day}")
        if period == "3":
            lists = AccountHistory.objects.filter(transaction_date__range = [f"{date - timedelta(3)}", f"{date}"])
        if period == "7":
            lists = AccountHistory.objects.filter(transaction_date__range = [f"{date - timedelta(7)}", f"{date}"])
        if period == "30":
            lists = AccountHistory.objects.filter(transaction_date__range = [f"{date - timedelta(30)}", f"{date}"])
        if period == "90":
            lists = AccountHistory.objects.filter(transaction_date__range = [f"{date - timedelta(90)}", f"{date}"])

        if start and end:
            lists = AccountHistory.objects.filter(transaction_date__range = [f"{start}", f"{end}"])

        if year and month:
            lists = AccountHistory.objects.filter(transaction_date__year = f"{year}", transaction_date__month = f"{month}")

        q = Q()
        if period == "1":
            q &= Q(transaction_date__day = f"{date.day-1}")
        if period == "0":
            q &= Q(transaction_date__day = f"{date.day}")
        if period == "3":
            q &= Q(transaction_date__range = [f"{date - timedelta(3)}", f"{date}"])
        if period == "7":
            q &= Q(transaction_date__range = [f"{date - timedelta(7)}", f"{date}"])
        if period == "30":
            q &= Q(transaction_date__range = [f"{date - timedelta(30)}", f"{date}"])
        if period == "90":
            q &= Q(transaction_date__range = [f"{date - timedelta(90)}", f"{date}"])
        
        if start and end:
            q &= Q(transaction_date__range = [f"{start}", f"{end}"])
        
        if year and month:
            q &= Q(transaction_date__year = f"{year}", transaction_date__month = f"{month}")

        
        if kind:
            if kind == "deposit":
                lists = AccountHistory.objects.filter(kind = "deposit").filter(q)
            elif kind == "withdraw":
                lists = AccountHistory.objects.filter(kind = "withdraw").filter(q)
        
        return lists
