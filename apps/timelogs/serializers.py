from rest_framework import serializers

from .models import TimeLog


class TimelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        exclude = ("owner",)


class TimelogStartTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ('task',)


class TimelogEndTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ('task',)
