from django.urls import path
from . views import get_url, save_apis, save_integration, get_token

urlpatterns = [
    path('keys', save_apis, name='save_apis'),
    path('integration', save_integration, name='save_integration'),
    path('url', get_url, name='get_url'),
    path('token', get_token, name='get_token'),
]
