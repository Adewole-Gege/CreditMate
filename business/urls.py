from django.urls import path
from .views import BusinessListCreateView, BusinessRetrieveUpdateDeleteView

urlpatterns = [
    path('businesses/', BusinessListCreateView.as_view(), name='business-list-create'),
    path('businesses/<int:id>/', BusinessRetrieveUpdateDeleteView.as_view(), name='business-detail'),
]