from django.db import models


class Wallet(models.Model):
    label = models.TextField()
    balance = models.DecimalField(max_digits=36, decimal_places=18, default=0)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    txid = models.CharField(max_length=36, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
