from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Business
from .serializers import BusinessSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    queryset = Business.objects.all()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Business.objects.none()

        return Business.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
