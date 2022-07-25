from rest_framework.exceptions import ValidationError
from raven.contrib.django.raven_compat.models import client
from rest_framework import serializers
import mysite.models as models

import sys


def get_exc_info():
    exc_info = sys.exc_info()
    if exc_info[0] is None:
        return None
    return exc_info


def capture_exception(error):
    exc_info = get_exc_info()
    if exc_info:
        client.captureException(exc_info)
    else:
        client.captureMessage(error)


class BaseInputSerializer(serializers.Serializer):
    class Meta:
        abstract = True

    def get_data_or_response(self):
        if not self.is_valid():
            capture_exception(self.errors)
            raise ValidationError(self.errors)
        return self.data


class UserRegistrationInputSerializer(BaseInputSerializer):
    username = serializers.CharField(max_length=150)
    password1 = serializers.CharField(max_length=32)
    password2 = serializers.CharField(max_length=32)


class UserLoginInputSerializer(BaseInputSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=32)


class FollowInputSerializer(BaseInputSerializer):
    target_username = serializers.CharField(max_length=150)
