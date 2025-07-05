from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('business.urls')),
    path('api/', include('ingestion.urls')),
    path('api/', include('scoring.urls')),
    path('api/', include('audit.urls')),
    path('api/', include('users.urls'))
]
