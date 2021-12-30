from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework import exceptions
from topics.models import AppUser
from topics.serializers import AppUserSerializer
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        password = request.data['password']
        confirmPassword = request.data['confirmPassword']
        
        if  password != confirmPassword:
            return Response({
                'message': 'Passwords do not match.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        appuser = AppUser()
        appuser.username = request.data['username']
        appuser.selectedTopicId=""
        appuser.topic=[]
        
        appuser.save()
        appuserserializer = AppUserSerializer(appuser)
        serializer.save()
        return Response(appuserserializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        user = User.objects.filter(username=username).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('User Not Found')
        
        if user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password')
        
        payload = { 
            "id": user.id, 
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'success'
        }
        
        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise exceptions.AuthenticationFailed('Unduthenticated')
        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        
        user = User.objects.filter(id=payload['id']).first()
        
        appuser = AppUser.objects.filter(username=user.username).first()
        
        appuserserializer = AppUserSerializer(appuser)
        
        print(AppUser.objects.all())
        
        return Response(appuserserializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response