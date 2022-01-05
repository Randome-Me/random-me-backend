from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import exceptions
from topics.models import AppUser
from topics.serializers import AppUserSerializer
import jwt

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        password = request.data['password']
        confirmPassword = request.data['confirmPassword']
        
        if password != confirmPassword:
            return Response({
                'message': 'Passwords do not match.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        appuser = AppUser()
        appuser.username = request.data['username']
        appuser.language = request.data['language']
        appuser.selectedTopicId=None
        appuser.topics=[]
        
        appuser.save()
        user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
        
        payload = { 
            "id": user.id, 
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
    
        appuserserializer = AppUserSerializer(appuser._id, appuser.username, appuser.language, appuser.selectedTopicId, appuser.topics)
        
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = appuserserializer.data
        response.status = status.HTTP_201_CREATED
        
        return response
    
class GuestRegisterView(APIView):
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        password = request.data['password']
        confirmPassword = request.data['confirmPassword']
        
        if password != confirmPassword:
            return Response({
                'message': 'Passwords do not match.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        appuser = AppUser()
        appuser.username = request.data['username']
        appuser.language = request.data['language']
        appuser.selectedTopicId = request.data['selectedTopicId']
        appuser.topics = request.data['topics']
        
        appuser.save()
        user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
        
        user = User.objects.filter(username=request.data['username']).first()
        
        payload = { 
            "id": user.id, 
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
    
        
        
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "_id": str(appuser._id)
        }
        response.status = status.HTTP_201_CREATED
        
        return response

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        user = User.objects.filter(username=username).first()
        
        print(password)
        print(check_password(password, user.password))
        
        if user is None or (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('Invalid username or password')
        
        payload = { 
            "id": user.id, 
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        appuser = AppUser.objects.get(username=user.username)
        appuserserializer = AppUserSerializer(appuser._id, appuser.username, appuser.language, appuser.selectedTopicId, appuser.topics)
        
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = appuserserializer.data
        
        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise exceptions.AuthenticationFailed('Unauthenticated')
        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        
        user = User.objects.get(id=payload['id'])
        
        appuser = AppUser.objects.get(username=user.username)
        appuserserializer = AppUserSerializer(appuser._id, appuser.username, appuser.language, appuser.selectedTopicId, appuser.topics)
        return Response(appuserserializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response