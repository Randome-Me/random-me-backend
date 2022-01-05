from django.db.models import fields
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
from .models import ResetPasswordToken
from users.customResponse import *
from datetime import datetime
import jwt, uuid

# Create your models here.
class ChangeLanguageAPIView(APIView):
    # /accounts/language/
    
    # {language:str}, Change user's default language
    def patch(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            return UserNotFoundResponse()
        
        appuser = AppUser.objects.get(username=user.username)
        
        if request.data['language'] is None or request.data['language'] not in ['en', 'th']:
            return InvalidFieldResponse(language=appuser.language)
        
        print(appuser.language)
        
        appuser.language = request.data['language']
        
        appuser.save(update_fields=['language'])
        
        return SuccessResponse(request.data['language'])
    
class ForgotPasswordAPIView(APIView):
    # /accounts/forgot-password/
    
    # {email:str}, Send email to change password 
    def post(self, request):
        
        user = User.objects.filter(email=request.data['email']).first()
        if user is None:
            return InvalidEmailResponse()
        
        resetpasswordtoken = ResetPasswordToken(userId=user.id, uuidToken=uuid.uuid4())
        
        payload = { 
            "uuidToken": str(resetpasswordtoken.uuidToken), 
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
        
        resetpasswordtoken.save()
        
        return SuccessResponse()
    
class ResetPasswordAPIView(APIView):
    # /accounts/reset-password/
    
    # {token:str, newPassword:str, language:str}, Change Password
    def post(self, request):
        
        if('language' in request.data):
            language = request.data['language']
        else:
            language = 'en'
        
        try:
            payload = jwt.decode(request.data['token'], 'secret', algorithms=['HS256'])
        except:
            return CustomErrorResponse()
        
        resetpasswordtoken = ResetPasswordToken.objects.filter(uuidToken=payload['uuidToken']).first()
        
        if resetpasswordtoken is None:
            return CustomErrorResponse(language=language)
        
        if resetpasswordtoken.expDate < datetime.now():
            return ExpiredLinkResponse(language=language)
        
        user = User.objects.filter(id=resetpasswordtoken.userId).first()
        user.set_password(request.data['newPassword'])
        user.save(update_fields=['password'])
        resetpasswordtoken.delete()
        
        return SuccessResponse(language=language)