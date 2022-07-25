from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone = PhoneNumberField(blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

class Token(models.Model):
    token = models.CharField(_("토큰"), max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)