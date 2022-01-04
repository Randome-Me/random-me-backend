from django.urls import path, include
from .views import *
from topics.models import *

urlpatterns = [
    path('language/', ChangeLanguageAPIView.as_view())
]