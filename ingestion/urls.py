from django.urls import path

from ingestion.views import UploadBankStatementView, DownloadBankStatementView

urlpatterns = [
      path(
        'upload-statement/<int:business_id>/',
        UploadBankStatementView.as_view(),
        name='upload-statement'),
      path(
        'download-statement/<uuid:statement_id>/',
        DownloadBankStatementView.as_view(),
        name='download-statement'),
]
