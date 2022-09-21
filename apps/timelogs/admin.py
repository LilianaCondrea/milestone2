from .models import TimeLog
from django.contrib import admin


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_timer', 'end_timer', 'task', 'owner')
