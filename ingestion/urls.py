from django.urls import path

from ingestion.views import upload_transactions, get_business_transactions

urlpatterns = [
    path('upload-transactions/<int:business_id>',
         upload_transactions,
         name='upload-transactions'),
    path('get-transactions/<int:business_id>',
         get_business_transactions,
         name='get-transactions'),
]
