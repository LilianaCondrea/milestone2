"""Task Serializers"""
from rest_framework import serializers
from .models import Task, Comment
from ..timelogs.serializers import TimeLogSerializer


class TaskSerializer(serializers.ModelSerializer):
    """TaskSerializer"""
    work_time = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'owner', 'work_time')


    def get_work_time(self, obj):
        if obj.work_time:
            return obj.work_time / 60
        return obj.work_time


class TaskSearchSerializer(serializers.ModelSerializer):
    """TaskSearchSerializer-for searching tasks"""
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    """TaskCreateSerializer-for creating tasks"""
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'owner')
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class TasksInfoSerializer(serializers.ModelSerializer):
    """TasksInfoSerializer-for returning tasks info"""
    class Meta:
        model = Task
        fields = ("id", "title")


class TaskUpdateSerializer(serializers.ModelSerializer):
    """TaskUpdateSerializer-for updating task's owner"""
    class Meta:
        model = Task
        fields = ("owner",)


class TaskUpdateStatusSerializer(serializers.ModelSerializer):
    """TaskUpdateSerializer-for updating task's status"""
    class Meta:
        model = Task
        fields = ("status",)


class CommentsSerializer(serializers.ModelSerializer):
    """CommentsSerializer"""
    class Meta:
        model = Comment
        fields = '__all__'


class TaskItemSerializer(serializers.ModelSerializer):
    """TaskItemSerializer"""
    comment_list = CommentsSerializer(source='comment_set', read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskItemLogsSerializer(serializers.ModelSerializer):
    """TaskItemLogsSerializer"""
    timelog_list = TimeLogSerializer(source='timelog_set', read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'
