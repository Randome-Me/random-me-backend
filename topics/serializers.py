from django.contrib.auth import models
from django.http.response import JsonResponse
from rest_framework import serializers
from .models import AppUser, Topic, Option
import json


class OptionSerializer:
    def __init__(self, dict):
        self.data = {
            "_id": None,
            "name": None,
            "bias": None,
            "pulls": None,
            "reward": None,
        }
        self.data["_id"] = dict["_id"]
        self.data["name"] = dict["name"]
        self.data["bias"] = dict["bias"]
        self.data["pulls"] = dict["pulls"]
        self.data["reward"] = dict["reward"]


class TopicSerializer:
    def __init__(self, dict):
        self.data = {
            "_id": None,
            "name": None,
            "policy": None,
            "t": None,
            "options": [],
        }
        self.data["_id"] = dict["_id"]
        self.data["name"] = dict["name"]
        self.data["policy"] = dict["policy"]
        self.data["t"] = dict["t"]
        if len(dict["options"]) > 0:
            self.data["options"] = [
                OptionSerializer(dict["options"][i]).data
                for i in range(len(dict["options"]))
            ]


class AppUserSerializer:
    def __init__(self, _id, username, email, language, selectedTopicId, topics):
        self.data = {
            "_id": None,
            "username": None,
            "email": None,
            "language": "en",
            "selectedTopicId": None,
            "topics": [],
        }
        self.data["_id"] = str(_id)
        self.data["username"] = username
        self.data["email"] = email
        self.data["language"] = language
        self.data["selectedTopicId"] = selectedTopicId
        if len(topics) > 0:
            self.data["topics"] = [
                TopicSerializer(topics[i]).data for i in range(len(topics))
            ]


# class AppUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppUser
#         fields = ['username', 'selectedTopicId', 'topics']

# class OptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Option
#         fields = ['name', 'bias', 'pulls', 'reward']

# class TopicSerializer(serializers.ModelSerializer):
#     options = OptionSerializer(many=True)
#     class Meta:
#         model = Topic
#         fields = ['name', 'policy', 't', 'options']

# class AppUserSerializer(serializers.ModelSerializer):
#     # topics = TopicSerializer(many=True)
#     class Meta:
#         model = AppUser
#         fields = ['username', 'selectedTopicId', 'topics']
