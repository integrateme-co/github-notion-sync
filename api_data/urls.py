from django.urls import path
from . views import get_url, get_user, get_webhook, save_apis, save_integration, get_token

urlpatterns = [
    path('keys', save_apis),
    path('integration', save_integration),
    path('url', get_url),
   # path('sync/<intID>',get_webhook ),
    path('token', get_token)
]