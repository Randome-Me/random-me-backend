from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from django.contrib.auth.models import User
from .models import AppUser
import jwt, uuid

# Create your views here.
class AddTopicView(APIView):
    #/topics/add
    def post(self, request):
        #name
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise exceptions.AuthenticationFailed('Unduthenticated')
        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        
        user = User.objects.get(id=payload['id'])
        
        appuser = AppUser.objects.get(username=user.username)

        appuser.topics.append({"_id":uuid.uuid4(),"name":request.data['name'], "policy":5, 't':0, "options":[]})
        
        appuser.save()
        
        response = Response()
        
        response.status = status.HTTP_201_CREATED
        response.data = {
            'message': 'success'
        }
        return response

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