from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

# Custom Response with specific language
class CustomErrorResponse(Response):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = {"en": "A server error occurred.", "th": "เกิดความผิดพลาด"}
    default_code = "error"
    default_language = "en"

    def __init__(self, code=None, language=None):
        if code is None:
            code = self.default_code
        if language is None:
            language = self.default_language
        super().__init__(
            data={"message": self.default_message[language]}, status=self.status_code
        )

    def __str__(self):
        return str(self.message)


class InvalidUsernameResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {
        "en": "Username must be between 4-20 characters and can contain any letters from a-z, A-Z, and 0-9.",
        "th": "ชื่อผู้ใช้ต้องมีความยาวระหว่าง 8-20 ตัวอักษี และประกอบไปด้วยตัวอักษร a-z, A-Z, หรือ 0-9",
    }
    default_code = "usernameAlreadyExist"


class UsernameAlreadyExistResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {
        "en": "This username is already exist.",
        "th": "ชื่อผู้ใช้นี้มีอยู่แล้วในระบบ",
    }
    default_code = "usernameAlreadyExist"


class EmailAlreadyUsedResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {
        "en": "This email is already used.",
        "th": "อีเมลนี้มีอยู่แล้วในระบบ",
    }
    default_code = "emailAlreadyUsed"


class InvalidPasswordResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {
        "en": "Password must be at least 8 characters and can contain any letters from a-z, A-Z, 0-9 and special characters (#,?,!,@,$,%,^,&,*,-).",
        "th": "รหัสผ่านต้องมีความยาว 8 ตัวอักษรขึ้นไป และประกอบไปด้วยตัวอักษร a-z, A-Z, 0-9 หรือตัวอักษรพิเศษ (#,?,!,@,$,%,^,&,*,-)",
    }
    default_code = "usernameAlreadyExist"


class InvalidEmailResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {"en": "Invalid email.", "th": "อีเมลไม่ถูกต้อง"}
    default_code = "invalidEmail"


class MismatchPasswordResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {"en": "Password did not match.", "th": "รหัสผ่านไม่ตรงกัน"}
    default_code = "mismatchPassword"


class UserNotFoundResponse(CustomErrorResponse):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = {"en": "User not found.", "th": "ไม่มีผู้ใช้นี้"}
    default_code = "userNotFound"


class UnauthenticatedResponse(CustomErrorResponse):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = {"en": "Has not log in.", "th": "ยังไม่ได้เข้าสู่ระบบ"}
    default_code = "unauthenticated"


class AuthenticationFailedResponse(CustomErrorResponse):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = {
        "en": "Invalid username or password.",
        "th": "ชื้อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
    }
    default_code = "authenticationFailed"


class InvalidTopicResponse(CustomErrorResponse):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = {"en": "Invalid topic.", "th": "หัวข้อไม่ถูกต้อง"}
    default_code = "invalidTopic"


class InvalidOptionResponse(CustomErrorResponse):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = {"en": "Invalid optioin.", "th": "ตัวเลือกไม่ถูกต้อง"}
    default_code = "invalidOption"


class InvalidFieldResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {
        "en": "Invalid field value.",
        "th": "ไม่สามารถเปลี่ยนข้อมูลที่ต้องการได้",
    }
    default_code = "invalidOption"


class ExpiredLinkResponse(CustomErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = {
        "en": "This link is already expired.",
        "th": "ลิงค์นี้หมดอายุแล้ว",
    }
    default_code = "expiredLinkResponse"


class InvalidTokenResponse(CustomErrorResponse):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = {"en": "Invalid token.", "th": "โทเคนไม่ถูกต้อง"}
    default_code = "invaidToken"


class SuccessResponse(CustomErrorResponse):
    status_code = status.HTTP_200_OK
    default_message = {"en": "Success.", "th": "สำเร็จ"}
    default_code = "success"


class CreatedResponse(CustomErrorResponse):
    status_code = status.HTTP_201_CREATED
    default_message = {"en": "Created.", "th": "สร้างสำเร็จ"}
    default_code = "crated"


class ChangePasswordSuccessResponse(CustomErrorResponse):
    status_code = status.HTTP_200_OK
    default_message = {
        "en": "Change password success.",
        "th": "กาเรปลี่ยนรหัสผ่านสำเร็จ",
    }
    default_code = "chagePasswordSuccess"


class SendMailSuccessResponse(CustomErrorResponse):
    status_code = status.HTTP_200_OK
    default_message = {
        "en": "How to reset your password is sent to your email. If you don't see it in your inbox, please check your spam folder.",
        "th": "วิธีการเปลี่ยนรหัสผ่านถูกส่งไปยังอีเมลของคุณแล้ว หากคุณไม่ได้รับอีเมลนี้ กรุณาตรวจสอบกล่องข้อความขยะของอีเมลของคุณ",
    }
    default_code = "sendMailSuccess"
