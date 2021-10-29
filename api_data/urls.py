from django.urls import path
from . views import get_user, get_webhook, save_apis, save_integration, get_token

urlpatterns = [
    path('keys', save_apis),
    path('integration', save_integration),
   # path('sync/<intID>',get_webhook ),
    path('token', get_token)
]