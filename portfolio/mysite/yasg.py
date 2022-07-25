from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

schema_url_patterns = [
    path('/', include('mysite.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title='LiveConnect-mysite User API',
        default_version='v1.0',
        description='''
        LiveConnect User API 문서 페이지입니다.
        API-KEY는 django admin - API-KEY에서 발급해야 하며
        Token 사용 시 "Bearer {Value}" 형식을 사용해야 합니다.
        ''',
        terms_of_service="https://www.google.com/policies/terms/"
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny, ),
    patterns=schema_url_patterns,
)
