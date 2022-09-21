from rest_framework import serializers

from .models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'owner')


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

