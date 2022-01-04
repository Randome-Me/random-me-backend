from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from django.contrib.auth.models import User
from topics.models import AppUser
import jwt

# Create your models here.
class ChangeLanguageAPIView(APIView):
    # /accounts/language/
    
    # {language:str}, Change user's default language
    def patch(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            return Response({"message":"User is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appuser = AppUser.objects.get(username=user.username)
        
        if request.data['language'] is None or request.data['language'] not in ['en', 'th']:
            return Response({"message":"Incorrect 'language' value"}, status=status.HTTP_400_BAD_REQUEST)
        
        print(appuser.language)
        
        appuser.language = request.data['language']
        
        appuser.save(update_fields=['language'])
        
        response = Response()
        response.status = status.HTTP_204_NO_CONTENT
        return response