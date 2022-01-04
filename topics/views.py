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
    
    # {_id:string, name:string}, Add topic
    def post(self, request):    
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)

        appuser.topics.append({"_id":request.data['_id'],"name":request.data['name'], "policy":5, "t":0, "options":[]})
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        
        response.status = status.HTTP_201_CREATED
        return response
    
    # {_id:string}, Select this topicId
    def patch(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)
        
        appuser.selectedTopicId = request.data['_id']
        appuser.save(update_fields=['selectedTopicId'])
        
        response = Response()
        response.status = status.HTTP_204_NO_CONTENT
        return response

class TopicsGenericAPIView(MultipleFieldLookupMixin, generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    # /topics/<str:topicId>/
    
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
        
        foundTopic = False
        
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                foundTopic = True
                appuser.topics[i]['options'].append({"_id":request.data['_id'], "name":request.data['name'], "bias":request.data['bias'], "pulls":0, "reward":0})
                break
        
        if not foundTopic:
            return Response({"message":"invalid topicId"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_201_CREATED
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
        
        foundTopic = False
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                foundTopic = True
                appuser.topics[i][request.data['field']] = request.data['value']
                break
        
        if not foundTopic:
            return Response({"message":"invalid topicId"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_204_NO_CONTENT
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
        
        foundTopic = False
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                foundTopic = True
                del appuser.topics[i]
                break
        
        if not foundTopic:
            return Response({"message":"invalid topicId"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_204_NO_CONTENT
        return response
        
class OptionGenericAPIView(MultipleFieldLookupMixin, generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    # /topics/<str:topicId>/<str:optionId>/
    
    lookup_field = ('topicId', 'optionId')
    
    # {reward:int}, Add option to topic
    def post(self, request, topicId, optionId):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)
        
        foundTopic = False
        foundOption = False
        
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                foundTopic = True
                for j in range(len(appuser.topics[i]['options'])):
                    if appuser.topics[i]['options'][j]['_id'] == optionId :
                        foundOption = True
                        appuser.topics[i]['t'] += 1
                        appuser.topics[i]['options'][j]['pulls'] += 1
                        appuser.topics[i]['options'][j]['reward'] += request.data['reward']
                        break
                break
        
        if not foundTopic:
            return Response({"message":"invalid topicId"}, status=status.HTTP_404_NOT_FOUND)
        
        if not foundOption:
            return Response({"message":"invalid optionId"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_204_NO_CONTENT
        return response
        
    # {field:string, value:string}, Change topic name/bias
    def patch(self, request, topicId, optionId):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)
        
        if request.data['field'] is None or request.data['field'] not in ['name', 'bias']:
            return Response({"message":"Incorrect 'field' value"}, status=status.HTTP_400_BAD_REQUEST)
        
        foundTopic = False
        foundOption = False
        
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                foundTopic = True
                for j in range(len(appuser.topics[i]['options'])):
                    if appuser.topics[i]['options'][j]['_id'] == optionId :
                        foundOption = True
                        appuser.topics[i]['options'][j][request.data['field']] = request.data['value']
                        break
                break
        
        if not foundTopic:
            return Response({"message":"invalid topicId"}, status=status.HTTP_404_NOT_FOUND)
        
        if not foundOption:
            return Response({"message":"invalid optionId"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_204_NO_CONTENT
        return response
    
    # Delete this topic
    def delete(self, request, topicId, optionId):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)
        
        foundTopic = False
        foundOption = False
        
        for i in range(len(appuser.topics)):
            if appuser.topics[i]['_id'] == topicId:
                foundTopic = True
                for j in range(len(appuser.topics[i]['options'])):
                    if appuser.topics[i]['options'][j]['_id'] == optionId :
                        foundOption = True
                        appuser.topics[i]['t'] -= appuser.topics[i]['options'][j]['pulls']
                        del appuser.topics[i]['options'][j]
                        break
                break
        
        if not foundTopic:
            return Response({"message":"invalid topicId"}, status=status.HTTP_404_NOT_FOUND)
        
        if not foundOption:
            return Response({"message":"invalid optionId"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser.save(update_fields=['topics'])
        
        response = Response()
        response.status = status.HTTP_204_NO_CONTENT
        return response