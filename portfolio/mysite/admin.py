from django.contrib import admin
from mysite.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields=['username',]


admin.site.register(Token)