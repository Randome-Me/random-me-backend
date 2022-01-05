from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

# Custom Response with specific language
class CustomErrorResponse(Response):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = {"en": "A server error occurred.", "th": "เกิดความผิดพลาด"}
    default_code = 'error'
    default_language = 'en'

    def __init__(self, code=None, language=None):
        if code is None:
            code = self.default_code
        if language is None:
            language = self.default_language
        super().__init__(data={'message': self.default_message[language]}, status=self.status_code)
        
    def __str__(self):
        return str(self.message)

class UsernameAlreadyExistResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {"en": "This username is already exist.", "th": "ชื่อผู้ใช้นี้มีอยู่แล้วในระบบ"}
    default_code = 'usernameAlreadyExist'

class EmailAlreadyUsedResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {"en": "This email is already used.", "th": "อีเมลนี้มีอยู่แล้วในระบบ"}
    default_code = 'emailAlreadyUsed'

class InvalidEmailResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {"en": "Invalid email.", "th": "อีเมลไม่ถูกต้อง"}
    default_code = 'invalidEmail'

class MismatchPasswordResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {"en": "Password did not match.", "th": "รหัสผ่านไม่ตรงกัน"}
    default_code = 'mismatchPassword'
    
class UserNotFoundResponse(CustomErrorResponse):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = {"en": "User not found.", "th": "ไม่มีผู้ใช้นี้"}
    default_code = 'userNotFound'

class UnauthenticatedResponse(CustomErrorResponse):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = {"en": "Has not log in.", "th": "ยังไม่ได้เข้าสู่ระบบ"}
    default_code = 'unauthenticated'
    
class AuthenticationFailedResponse(CustomErrorResponse):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = {"en": "Invalid username or password.", "th": "ชื้อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"}
    default_code = 'authenticationFailed'
    
class InvalidTopicResponse(CustomErrorResponse):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = {"en": "Invalid topic.", "th": "หัวข้อไม่ถูกต้อง"}
    default_code = 'invalidTopic'
   
class InvalidOptionResponse(CustomErrorResponse):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = {"en": "Invalid optioin.", "th": "ตัวเลือกไม่ถูกต้อง"}
    default_code = 'invalidOption'
    
class InvalidFieldResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {"en": "Invalid field value.", "th": "ไม่สามารถเปลี่ยนข้อมูลที่ต้องการได้"}
    default_code = 'invalidOption'
    
class SuccessResponse(CustomErrorResponse):
    status_code = status.HTTP_200_OK
    default_message = {"en": "Success.", "th": "สำเร็จ"}
    default_code = 'success'
    

class CreatedResponse(CustomErrorResponse):
    status_code = status.HTTP_201_CREATED
    default_message = {"en": "Created.", "th": "สร้างสำเร็จ"}
    default_code = 'crated'