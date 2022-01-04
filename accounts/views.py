from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from django.contrib.auth.models import User
from topics.models import AppUser
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
    
class ForgotPasswordAPIView(APIView):
    # /accounts/reset_password
    
    # {email:str}, Send email to change password 
    def post(self, request):
        
        user = User.objects.filter(email=request.data['email']).first()
        if user is None:
            return Response({"message":"No user with this email"}, status=status.HTTP_404_NOT_FOUND)
        
        payload = { 
            "id": user.id, 
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        link = str(settings.CHANGE_PASSWORD_PAGE) + '?token=' + token
        
        html_message = render_to_string('accounts/mail_template.html', context={'link': link})
        
        mail.send_mail(
            subject='RandomMe: Change Your Password', 
            message=strip_tags(html_message), 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[user.email],
            html_message=html_message
        )
        
        response = Response()
        response.status = status.HTTP_200_OK
        return response