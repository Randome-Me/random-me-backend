from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from django.contrib.auth.models import User
from .serializers import AppUserSerializer
from .models import *

# Create your views here.
class AddTopicView(APIView):
    #/topics/add
    def post(self, request):
        #name
        pass

class AddOptionView(APIView):
    #/options/add
    def post(self, request):
        #name + weight
        pass
    
class SetTopicNameView(APIView):
    #/topics/name
    def post(self, request):
        #topicId + name
        pass
    
class SetOptionNameView(APIView):
    #/options/name
    def post(self, request):
        #optionId + name
        pass
    
class SetBiasView(APIView):
    #/topics/bias
    def post(self, request):
        #optionId + bias
        pass

class SelectView(APIView):
    #/topics/select
    def post(self, request):
        #topicId
        pass
    
class ChangePolicyView(APIView):
    #/topics/policy
    def post(self, request):
        #topicId + policy
        pass
    
class PullArmView(APIView):
    #/topics/pull
    def post(self, request):
        #optionId + reward
        pass

class RemoveOptionView(APIView):
    #/options/remove
    def post(self, request):
        #optionId
        pass
    
class RemoveTopicView(APIView):
    #/topics/remove
    def post(self, request):
        #topicId
        pass
