from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api_data.views import redirect_view

schema_view = get_schema_view(
   openapi.Info(
      title="integrateme.co API Docs",
      default_version='v1',
      description="API Documentation for github-notion sync and save API keys",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="hey@integrateme.co"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('save/', include('api_data.urls')),
    path('github-notion/sync/', include('gh_sync.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', redirect_view, name='redirect'),
]