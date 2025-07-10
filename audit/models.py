from django.db import models
from business.models import Business
from ingestion.models import BankStatement

class ScoreAuditLog(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    risk_level = models.CharField(max_length=20)
    version = models.CharField(max_length=50)
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business.name} - {self.score} ({self.risk_level})"
