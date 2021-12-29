from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework import exceptions
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
        
        serializer.save()
        return Response(serializer.data)
