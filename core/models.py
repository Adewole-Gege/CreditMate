# core/models.py
from django.db import models
from business.models import SME


class CreditScore(models.Model):
    sme = models.OneToOneField(SME, on_delete=models.CASCADE, related_name='credit_score')
    score = models.PositiveIntegerField()
    risk_level = models.CharField(max_length=20)
    data_version = models.CharField(max_length=30)
    calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sme.business_name} - {self.score} ({self.risk_level})"


# Optional: Add index if needed for faster lookup
    class Meta:
        indexes = [
            models.Index(fields=['risk_level']),
        ]