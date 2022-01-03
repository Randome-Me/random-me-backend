from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import AppUser
from .customMixins import MultipleFieldLookupMixin
import jwt, uuid

# Create your views here.
class AddTopicView(APIView):    
    # /topics/
    
    def post(self, request):    # {name:string}, Add topic
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)

        appuser.topics.append({"_id":uuid.uuid4(),"name":request.data['name'], "policy":5, "t":0, "options":[]})
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        
        response.status = status.HTTP_201_CREATED
        response.data = {
            'message': 'success'
        }
        return response

class TopicsGenericAPIView(MultipleFieldLookupMixin, generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    # <str:topicId>/
    
    lookup_field = 'topicId'
    
    # {name:string, bias:int}, Add option to topic
    def post(self, request, topicId):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)
        
        found = False
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                found = True
                appuser.topics[i]['options'].append({"_id":uuid.uuid4(),"name":request.data['name'], "bias":request.data['bias'], "pulls":0, "reward":0})
                break
        
        if not found:
            return Response({"message":"Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_201_CREATED
        response.data = {
            'message': 'success'
        }
        return response
    
    # Select this topicId
    def put(self, request, topicId):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        appuser = AppUser.objects.get(username=user.username)
        
        appuser.selectedTopicId = topicId
        appuser.save(update_fields=['selectedTopicId'])
        
        response = Response()
        response.status = status.HTTP_201_CREATED
        response.data = {
            'message': 'success'
        }
        return response
        
    # {field:string, value:string}, Change topic name/policy
    def patch(self, request, topicId):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)
        
        if request.data['field'] is None or request.data['field'] not in ['name', 'policy']:
            return Response({"message":"Incorrect 'field' value"}, status=status.HTTP_400_BAD_REQUEST)
        
        found = False
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                found = True
                appuser.topics[i][request.data['field']] = request.data['value']
                break
        
        if not found:
            return Response({"message":"Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_200_OK
        response.data = {
            'message': 'success'
        }
        return response
    
    # Delete this topic
    def delete(self, request, topicId):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)
        
        found = False
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                found = True
                del appuser.topics[i]
                break
        
        if not found:
            return Response({"message":"Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_200_OK
        response.data = {
            'message': 'success'
        }
        return response
        
    
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