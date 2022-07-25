from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from mysite.views import *
from .yasg import *




urlpatterns = [
    path("", index, name="index"),

    path(
        'swagger<str:format>',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
	path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    path('api/user/signup', UserRegistrationAPIViw.as_view(), name='api-user-signup'),
    path('api/user/login', UserLoginAPIView.as_view(), name='api-user-login'),
    path('api/user/logout', UserLogoutAPIView.as_view(), name='api-user-logout'),

    path('api/user/info', UserInfoAPIView.as_view(), name='api-user-info'),
    path('api/user/list', UserListAPIView.as_view(), name='api-user-list'),
    path('api/follow', FollowAPIView.as_view(), name='api-follow'),

    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)