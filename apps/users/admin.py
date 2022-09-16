# Register your models here.
from .models import User
from django.contrib import admin
from django.contrib.admin import ModelAdmin


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    list_display = ['id', 'email']
