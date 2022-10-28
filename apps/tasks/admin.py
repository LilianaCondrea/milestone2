from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'status', 'owner')


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
