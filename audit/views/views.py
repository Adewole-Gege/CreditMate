from rest_framework import viewsets
from .models import AuditLog
from .serializers import AuditLogSerializer
import logging

logger = logging.getLogger("audit_logger")

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        log_entry = f"[{instance.timestamp}] {instance.category.upper()} | UserID: {instance.user_id} | {instance.action_type} | {instance.description}"
        logger.info(log_entry)

