import uuid
from django.db import models

from business.models import Business


class BankStatement(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='bank_statements'
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    statement_file = models.TextField()

    encoded_data = models.TextField(
        help_text='Base64 or JSON encoded transaction data'
    )

    start_date = models.DateField()
    end_date = models.DateField()

    total_income = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_expenditure = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'reference'],
                name='unique_bank_statement_ref_per_business'
            )
        ]

    def __str__(self):
        return f"{self.reference} ({self.business.name})"


# ingestion/models.py
class BankTransaction(models.Model):
    statement = models.ForeignKey('BankStatement', related_name='transactions', on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    transaction_type = models.CharField(max_length=10)  # credit or debit
    channel = models.CharField(max_length=20, null=True, blank=True)
    counterparty = models.CharField(max_length=100, null=True, blank=True)
