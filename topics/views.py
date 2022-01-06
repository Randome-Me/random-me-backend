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
from users.customResponse import *
import jwt, uuid

# Create your views here.
class AddTopicView(APIView):
    # /topics/

    # {_id:string, name:string}, Add topic
    def post(self, request):
        token = request.COOKIES.get("jwt")
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        if user is None:
            return UserNotFoundResponse()

        appuser = AppUser.objects.get(username=user.username)

        appuser.topics.append(
            {
                "_id": request.data["_id"],
                "name": request.data["name"],
                "policy": 5,
                "t": 0,
                "options": [],
            }
        )

        appuser.save(update_fields=["topics"])

        return CreatedResponse(language=appuser.language)

    # {_id:string}, Select this topicId
    def patch(self, request):
        token = request.COOKIES.get("jwt")
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        if user is None:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        appuser = AppUser.objects.get(username=user.username)

        appuser.selectedTopicId = request.data["_id"]
        appuser.save(update_fields=["selectedTopicId"])

        return SuccessResponse(language=appuser.language)


class TopicsGenericAPIView(
    MultipleFieldLookupMixin,
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    # /topics/<str:topicId>/

    lookup_field = "topicId"

    # {_id: string, name:string, bias:int}, Add option to topic
    def post(self, request, topicId):
        token = request.COOKIES.get("jwt")
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        if user is None:
            return UserNotFoundResponse()

        appuser = AppUser.objects.get(username=user.username)

        foundTopic = False

        for i in range(len(appuser.topics)):
            if appuser.topics[i]["_id"] == topicId:
                foundTopic = True
                appuser.topics[i]["options"].append(
                    {
                        "_id": request.data["_id"],
                        "name": request.data["name"],
                        "bias": request.data["bias"],
                        "pulls": 0,
                        "reward": 0,
                    }
                )
                break

        if not foundTopic:
            return InvalidTopicResponse(language=appuser.language)

        appuser.save(update_fields=["topics"])

        return CreatedResponse(language=appuser.language)

    # {field:string, value:string}, Change topic name/policy
    def patch(self, request, topicId):
        token = request.COOKIES.get("jwt")
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        if user is None:
            return UserNotFoundResponse()

        appuser = AppUser.objects.get(username=user.username)

        if request.data["field"] is None or request.data["field"] not in [
            "name",
            "policy",
        ]:
            return Response(
                {"message": "Incorrect 'field' value"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        foundTopic = False
        for i in range(len(appuser.topics)):
            if appuser.topics[i]["_id"] == topicId:
                foundTopic = True
                appuser.topics[i][request.data["field"]] = request.data["value"]
                break

        if not foundTopic:
            return InvalidTopicResponse(language=appuser.language)

        appuser.save(update_fields=["topics"])

        return SuccessResponse(language=appuser.language)

    # Delete this topic
    def delete(self, request, topicId):
        token = request.COOKIES.get("jwt")
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        if user is None:
            return UserNotFoundResponse()

        appuser = AppUser.objects.get(username=user.username)

        foundTopic = False
        for i in range(len(appuser.topics)):
            if appuser.topics[i]["_id"] == topicId:
                foundTopic = True
                del appuser.topics[i]
                break

        if not foundTopic:
            return InvalidTopicResponse(language=appuser.language)

        appuser.save(update_fields=["topics"])

        return SuccessResponse(language=appuser.language)


class OptionGenericAPIView(
    MultipleFieldLookupMixin,
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    # /topics/<str:topicId>/<str:optionId>/

    lookup_field = ("topicId", "optionId")

    # {reward:int}, Pull arm
    def post(self, request, topicId, optionId):
        token = request.COOKIES.get("jwt")
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        if user is None:
            return UserNotFoundResponse()

        appuser = AppUser.objects.get(username=user.username)

        foundTopic = False
        foundOption = False

        for i in range(len(appuser.topics)):
            if appuser.topics[i]["_id"] == topicId:
                foundTopic = True
                for j in range(len(appuser.topics[i]["options"])):
                    if appuser.topics[i]["options"][j]["_id"] == optionId:
                        foundOption = True
                        appuser.topics[i]["t"] += 1
                        appuser.topics[i]["options"][j]["pulls"] += 1
                        appuser.topics[i]["options"][j]["reward"] += request.data[
                            "reward"
                        ]
                        break
                break

        if not foundTopic:
            return InvalidTopicResponse(language=appuser.language)

        if not foundOption:
            return InvalidOptionResponse(language=appuser.language)

        appuser.save(update_fields=["topics"])

        return SuccessResponse(language=appuser.language)

    # {field:string, value:string}, Change topic name/bias
    def patch(self, request, topicId, optionId):
        token = request.COOKIES.get("jwt")
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        if user is None:
            return UserNotFoundResponse()

        appuser = AppUser.objects.get(username=user.username)

        if request.data["field"] is None or request.data["field"] not in [
            "name",
            "bias",
        ]:
            return InvalidFieldResponse(language=appuser.language)

        foundTopic = False
        foundOption = False

        for i in range(len(appuser.topics)):
            if appuser.topics[i]["_id"] == topicId:
                foundTopic = True
                for j in range(len(appuser.topics[i]["options"])):
                    if appuser.topics[i]["options"][j]["_id"] == optionId:
                        foundOption = True
                        appuser.topics[i]["options"][j][
                            request.data["field"]
                        ] = request.data["value"]
                        break
                break

        if not foundTopic:
            return InvalidTopicResponse(language=appuser.language)

        if not foundOption:
            return InvalidOptionResponse(language=appuser.language)

        appuser.save(update_fields=["topics"])

        return SuccessResponse(language=appuser.language)

    # Delete this topic
    def delete(self, request, topicId, optionId):
        token = request.COOKIES.get("jwt")
        if token is None:
            return UnauthenticatedResponse()
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        if user is None:
            return UserNotFoundResponse()

        appuser = AppUser.objects.get(username=user.username)

        foundTopic = False
        foundOption = False

        for i in range(len(appuser.topics)):
            if appuser.topics[i]["_id"] == topicId:
                foundTopic = True
                for j in range(len(appuser.topics[i]["options"])):
                    if appuser.topics[i]["options"][j]["_id"] == optionId:
                        foundOption = True
                        appuser.topics[i]["t"] -= appuser.topics[i]["options"][j][
                            "pulls"
                        ]
                        del appuser.topics[i]["options"][j]
                        break
                break

        if not foundTopic:
            return InvalidTopicResponse(language=appuser.language)

        if not foundOption:
            return InvalidOptionResponse(language=appuser.language)

        appuser.save(update_fields=["topics"])

        return SuccessResponse()
