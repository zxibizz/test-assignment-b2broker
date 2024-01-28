from rest_framework_json_api.views import ModelViewSet

from app.serializers import WalletSerializer, TransactionSerializer
from app.models import Wallet, Transaction


class WalletViewSet(ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    filterset_fields = {
        "id": ("exact",),
        "wallet_id": ("exact",),
        "txid": ("icontains", "exact"),
        "amount": ("exact", "lt", "gt", "gte", "lte"),
    }
