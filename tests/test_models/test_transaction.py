import pytest

from app.models import Wallet, Transaction


@pytest.fixture
def wallet():
    return Wallet.objects.create(label="test wallet")


@pytest.mark.django_db
def test_wallet_balance_is_updated(wallet):
    t1 = Transaction.objects.create(wallet_id=wallet.id, txid="1", amount=10)
    t2 = Transaction.objects.create(wallet_id=wallet.id, txid="2", amount=-5)

    wallet.refresh_from_db()
    assert wallet.balance == 5

    t1.amount = 12
    t1.save()

    wallet.refresh_from_db()
    assert wallet.balance == 7

    t2.delete()

    wallet.refresh_from_db()
    assert wallet.balance == 12
