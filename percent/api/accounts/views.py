from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions

from app.accounts.models import Account, AccountHistory
from app.user.models import User
from .serializers import TransactionSerializer

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
        if self.action in ['create']:
            self.permission_class = permissions.IsAuthenticated

        return super().get_permissions()
