from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi

from mysite.models import *
from mysite.forms.forms import UserRegistrationForm

import mysite.serializer as sz

import string
import json
import jwt
import datetime


#토큰 refresh 할 때 Token 모델에 추가해주기 위해 orverride
class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        Token.objects.create(token=data["access"])
        return data

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

#토큰정보 디코딩
def get_payload(request):
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    try:
        payload = jwt.decode(
            token,
            settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithms=settings.SIMPLE_JWT["ALGORITHM"],
        )
        exp = datetime.datetime.fromtimestamp(int(payload["exp"]))
        if datetime.datetime.now() > exp:
            tokens = Token.object.filter(token=token)
            if tokens:
                tokens.first.delete()

        return payload
    except ValidationError as v:
        return None

class UserRegistrationAPIView(GenericAPIView):
    permission_classes = [HasAPIKey,]
    parser_classes = [MultiPartParser,]

    # 회원가입
    @swagger_auto_schema(request_body=sz.UserRegistrationInputSerializer)
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return JsonResponse({"msg": f"{username} sign-up success."}, status=200)
        else:
            return JsonResponse({"msg": json.loads(form.errors.as_json())}, status=400)


class UserLoginAPIView(APIView):
    permission_classes = [HasAPIKey,]
    parser_classes = [MultiPartParser,]

    # 로그인
    @swagger_auto_schema(request_body=sz.UserLoginInputSerializer)
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        users = User.objects.filter(username=username)
        if users.exists():
            user = users.first()

            #JWT 발급
            serializer = TokenObtainPairSerializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                return JsonResponse({"msg": "Invalid Data."}, status=400)
            
            #로그아웃 시 토큰 정보를 삭제하기 위해 생성
            Token.objects.create(token=serializer.validated_data["access"])

            return JsonResponse(serializer.validated_data, status=200)
        else:   
            return JsonResponse({"msg": "user not found."}, status=400)


# 로그아웃
class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(request_body=no_body)
    def post(self, request, *args, **kwargs):
        payload = get_payload(request)
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        tokens = Token.objects.filter(token=token)
        
        #Token 모델에서 해당 token을 삭제하여 로그아웃 시키기
        if tokens.exists():
            token = tokens.first()
            token.delete()
            return JsonResponse({"msg": "Logout success"}, status=200)
        else:
            return JsonResponse({"msg": "Token not found."}, status=400)


# 마이페이지
class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(request_body=no_body)
    def get(self, request, *args, **kwargs):
        #토큰에서 유저id 가져오기
        payload = get_payload(request)

        #Token 모델에 토큰이 없으면 만료된 토큰으로 판단.
        token_value = request.META.get('HTTP_AUTHORIZATION',"").split(' ')[1]
        token_object = Token.objects.filter(token = token_value)

        if not token_object.exists():
            return JsonResponse({"msg":"token is expired."}, status=400)
        user_id = payload["user_id"]

        user = User.objects.filter(id=user_id)

        #유저가 조회되지 않을 경우
        if not user.exists():
            return JsonResponse({"msg": "User not found."}, status=400)

        result_data = sz.UserInfoSerializer(user, many=True).data
        return JsonResponse({"data":result_data, "msg":"success"}, status=200)

class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(request_body=no_body)
    def get(self, request, *args, **kwargs):
        #토큰에서 유저id 가져오기
        payload = get_payload(request)

        #Token 모델에 토큰이 없으면 만료된 토큰으로 판단.
        token_value = request.META.get('HTTP_AUTHORIZATION',"").split(' ')[1]
        token_object = Token.objects.filter(token = token_value)

        #토큰이 없을 경우 만료처리
        if not token_object.exists():
            return JsonResponse({"msg":"token is expired."}, status=400)
        user_id = payload["user_id"]

        user = User.objects.filter(id=user_id)

        if not user.exists():
            return JsonResponse({"msg": "User not found."}, status=400)

        if user.first().is_staff or user.first().is_superuser:
            users = User.objects.all()
            result_data = sz.UserInfoSerializer(users, many=True).data
            return JsonResponse({"data":result_data, "msg":"success"}, status=200)
        else:
            return JsonResponse({"data":{},"msg": "user is not admin."}, status=400)


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=sz.FollowInputSerializer)
    def post(self, request, *args, **kwargs):

        #토큰에서 유저id 가져오기
        payload = get_payload(request)

        #Token 모델에 토큰이 없으면 만료된 토큰으로 판단.
        token_value = request.META.get('HTTP_AUTHORIZATION',"").split(' ')[1]
        token_object = Token.objects.filter(token = token_value)

        if not token_object.exists():
            return JsonResponse({"msg":"token is expired."}, status=400)
        user_id = payload["user_id"]

        user = User.objects.filter(id=user_id)

        if not user.exists():
            return JsonResponse({"msg": "User not found."}, status=400)

        user = user.first()

        target_username = request.POST.get("target_username")
        target_user = User.objects.filter(username=target_username)

        # 팔로우 대상이 조회되지 않을경우
        if not target_user.exists():
            return JsonResponse({"msg": "Target User not found."}, status=400)
        target_user = target_user.first()

        # 팔로우 대상이 본인일 경우
        if target_user == user:
            return JsonResponse({"msg": "Can not follow self."}, status=400)

        #이미 팔로우 되어있을 경우
        following_list = user.following.all()
        if target_user in following_list:
            return JsonResponse({"msg": "already exist."}, status=400)

        #팔로잉 유저에 추가
        user.following.add(target_user)
        return JsonResponse({"msg": "success"}, status=200)
