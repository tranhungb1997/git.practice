from django.contrib import admin
from user.models import *


@admin.register(UserCustom)
class UserCustomAdmin(admin.ModelAdmin):
    list_display = ('username',)
