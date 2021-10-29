from django.urls import path
from .views import get_webhook

urlpatterns = [
    path('<intID>',get_webhook,name='get_webhook'),
]
