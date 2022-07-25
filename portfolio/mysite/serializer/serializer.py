from rest_framework import serializers
import mysite.models as models
import json

class UserInfoSerializer(serializers.ModelSerializer):
    follower_list = serializers.SerializerMethodField()
    following_list = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "follower_list",
            "following_list",
            "phone",
        )

    def get_follower_list(self, obj):
        return list(obj.followers.all().values_list("username", flat=True))

    def get_following_list(self, obj):
        return list(obj.following.all().values_list("username", flat=True))