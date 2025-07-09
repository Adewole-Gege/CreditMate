from .views import BusinessViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('businesses', BusinessViewSet, basename='business')

urlpatterns = router.urls