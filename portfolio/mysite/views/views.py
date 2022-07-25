from django.shortcuts import render
from django.views.generic import TemplateView

def index(request):
    return render(request, 'index.html')

class SignupView(TemplateView):
    template_name = "auth/signup.html"


class LoginView(TemplateView):
    template_name = "auth/login.html"


class LogoutView(TemplateView):
    template_name = "auth/logout.html"


class AuthTokenView(TemplateView):
    template_name = "auth/token.html"


class AuthTokenVerifyView(TemplateView):
    template_name = "auth/token_verify.html"


class AuthTokenRefreshView(TemplateView):
    template_name = "auth/token_refresh.html"


class FollowView(TemplateView):
    template_name = "auth/follow.html"