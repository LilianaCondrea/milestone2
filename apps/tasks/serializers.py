from rest_framework import serializers

from .models import Task, Comment
from ..timelogs.serializers import TimeLogSerializer


class TaskSerializer(serializers.ModelSerializer):
    work_time = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'owner')

    def get_work_time(self, obj):
        if obj.work_time:
            return obj.work_time / 60
        return obj.work_time


class TaskSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'owner')
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class TasksInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title")


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("owner",)


class TaskUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("status",)


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TaskItemSerializer(serializers.ModelSerializer):
    comment_list = CommentsSerializer(source='comment_set', read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskItemLogsSerializer(serializers.ModelSerializer):
    timelog_list = TimeLogSerializer(source='timelog_set', read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'
