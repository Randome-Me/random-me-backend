from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AddTopicView.as_view()),
    path('<str:topicId>/', TopicsGenericAPIView.as_view())
]