from django.db import models

class AuditLog(models.Model):
    CATEGORY_CHOICES = [
        ('user', 'User Activity'),
        ('document', 'Document Event'),
        ('financial', 'Financial Transaction'),
        ('system', 'System-Level Event'),
        ('security', 'Security & Compliance'),
        ('admin', 'Admin Action'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(null=True, blank=True)
    action_type = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    resource = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action_type}"

