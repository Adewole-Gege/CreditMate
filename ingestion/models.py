from django.db import models
import uuid

from business.models import Business


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    transaction_type = models.CharField(
        max_length=6,
        choices=TRANSACTION_TYPES
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    reference = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'reference'],
                name='unique_business_reference')]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['transaction_type']),]

    def __str__(self):
        return f"{self.reference} ({self.transaction_type}) - {self.amount}"
