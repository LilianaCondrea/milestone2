from rest_framework import serializers

from .models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        exclude = ("owner",)


class TimeLogStartTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ('task',)


class TimeLogEndTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ('task',)
