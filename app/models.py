from django.db import models, transaction


class Wallet(models.Model):
    label = models.TextField()
    balance = models.DecimalField(
        max_digits=36, decimal_places=18, default=0, editable=False
    )

    class Meta:
        ordering = ("id",)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    txid = models.CharField(max_length=36, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if update_fields is not None and "amount" not in update_fields:
            return super().save(force_insert, force_update, using, update_fields)

        with transaction.atomic():
            if not self.pk:
                Wallet.objects.filter(id=self.wallet_id).update(
                    balance=models.F("balance") + self.amount,
                )
            else:
                q = Transaction.objects.filter(id=self.id).values_list("amount")
                Wallet.objects.filter(id=self.wallet_id).update(
                    balance=models.F("balance") + self.amount - q[:1]
                )
            super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic():
            Wallet.objects.filter(id=self.wallet_id).update(
                balance=models.F("balance") - self.amount,
            )
            super().delete(using, keep_parents)

    class Meta:
        ordering = ("id",)
