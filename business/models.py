from django.db import models
from django.conf import settings
import uuid

class Business(models.Model):
    # Basic Info
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(
        max_length=255,
        unique=True
    )
    registration_number = models.CharField(
        max_length=100,
        unique=True
    )
    tax_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    industry = models.CharField(
        max_length=100
    )
    date_founded = models.DateField(
        null=True,
        blank=True
    )
    website = models.URLField(
        null=True,
        blank=True
    )

    # Contact Info
    email = models.EmailField(
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    address = models.TextField(
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=100
    )
    city = models.CharField(
        max_length=100
    )

    # Audit Fields
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='businesses'
    )

    class Meta:
        db_table = "businesses"
        ordering = [
            '-created_at'
        ]
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return f"{self.name}: ({self.registration_number})"