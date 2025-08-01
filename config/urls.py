from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from core.views import home_view

schema_view = get_schema_view(
    openapi.Info(
        title="CreditMate",
        default_version='v1',
        description="API documentation",
        contact=openapi.Contact(email="creditmate@creditmate.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/', include('business.urls')),
    path('api/', include('ingestion.urls')),
    path('api/', include('users.urls')),
    path('api/', include('core.urls')),
    path('', home_view, name="Home")
]