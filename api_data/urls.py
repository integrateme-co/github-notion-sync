from django.urls import path
from . views import get_user, save_apis, save_integration, get_token

urlpatterns = [
    path('user', get_user),
    path('save', save_apis),
    path('inte', save_integration),
    path('sync/<intID>',get_user ),
    path('token', get_token)
]