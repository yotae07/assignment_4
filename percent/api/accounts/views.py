from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from api.accounts.serializers import AccountHistorySerializer, AccountSerializer
from rest_framework.permissions import IsAuthenticated


class AccountViewSet(CreateModelMixin, GenericViewSet):
    serializers_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return AccountSerializer

    def create(self, request, *args, **kwargs):
        self.request.data.setdefault('user', self.request.headers["Authorization"])        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountHistoryViewSet(CreateModelMixin, GenericViewSet):

    serializer_class = AccountHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return AccountHistorySerializer

    def create(self, request, *args, **kwargs):
        self.request.data.setdefault('user', self.request.headers["Authorization"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
