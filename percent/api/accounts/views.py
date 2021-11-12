from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from api.accounts.serializers import AccountHistorySerializer
from rest_framework.permissions import IsAuthenticated

class AccountViewSet(CreateModelMixin, GenericViewSet):

    serializer_class = AccountHistorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
