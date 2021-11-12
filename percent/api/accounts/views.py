from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from app.accounts.models import Account, AccountHistory
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import AccountInfoSerializer


class AccountInfoViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = AccountHistory.objects.all()
    serializer_class = AccountInfoSerializer
    permission_classes = [IsAuthenticated, AllowAny]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated,AllowAny]  # -> custom
        return [permission() for permission in self.permission_classes]

    def get_queryset(self, start_date, end_date, trans_type, order):
        if order == '1':
            return AccountHistory.objects.filter(kind='trans_type', transaction_date__range=[start_date, end_date]).order_by("-transaction_date")
        else:
            return AccountHistory.objects.filter(kind='trans_type', transaction_date__range=[start_date, end_date]).order_by("transaction_date")

    def list(self, request, *args, **kwargs):
        start_date = self.request.query_params.get('start_date', )
        end_date = self.request.query_params.get('end_date', )
        trans_type = self.request.query_params.get('trans_type', '')
        order = self.request.query_params.get('order', '0')
        queryset = self.get_queryset(start_date, end_date, trans_type, order)
        serializer = self.get_serializer_class(queryset, many=True)
        return Response(serializer.data)
