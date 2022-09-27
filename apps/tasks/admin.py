"""Register models in django-admin."""
from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    """Register Task in django-admin."""
    list_display = ('id', 'title', 'description', 'status', 'owner')


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    """Register Comment in django-admin."""
    list_display = ('id', 'text')
