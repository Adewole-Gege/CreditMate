from django.db import models
from business.models import Business  # TODO: Ensure this import matches actual SME model location

# If SME is the same as Business, use Business. Otherwise, import the correct SME model.
# Here, we assume SME == Business for demonstration.

RISK_LEVEL_CHOICES = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
)

class CreditScore(models.Model):
    sme = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='credit_score')
    score = models.PositiveIntegerField(help_text="Credit score between 0 - 1000")
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, help_text="Automated risk classification based on score thresholds")
    data_version = models.CharField(max_length=50, default="v1-basic-rules", help_text="Version of the scoring logic applied")
    calculated_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when score was last calculated")

    class Meta:
        ordering = ['-calculated_at']
        verbose_name = "Credit Score"
        verbose_name_plural = "Credit Scores"
        indexes = [
            models.Index(fields=['sme']),
            models.Index(fields=['score']),
            models.Index(fields=['risk_level']),
        ]

    def __str__(self):
        return f"{self.sme.business_name} - Score: {self.score} ({self.risk_level})"