from datetime import timezone, timedelta

import django_filters
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.db.models import Sum, F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, filters
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Task, Comment
from .serializers import TaskCreateSerializer, TaskSerializer, \
    TaskUpdateSerializer, TaskUpdateStatusSerializer, CommentsSerializer, TaskSearchSerializer, TaskItemSerializer, \
    TaskItemLogsSerializer
from ..users.models import User
from ..users.serializers import GetUsersSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.annotate(work_time=Sum(F('timelog__end_time') - F('timelog__start_time')))
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    serializer_class = TaskSerializer

    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status=False)

    def destroy(self, request, *args, **kwargs):
        task = get_object_or_404(Task.objects.filter(pk=kwargs.get('pk')))
        task.delete()
        return Response({"success": True, "message": "task deleted successfully"})

    def list(self, request, *args, **kwargs):
        tasks = Task.objects.annotate(work_time=Sum(F('timelog__end_time') - F('timelog__start_time')))
        return Response(TaskSerializer(tasks, many=True).data)

    # @action(methods=['GET'], detail=False, serializer_class=TasksInfoSerializer)
    # def search(self, request):
    #     tasks = Task.objects.filter(owner=self.request.user)
    #     return Response(TasksInfoSerializer(tasks, many=True).data)
    #
    # @action(methods=['GET'], detail=False, serializer_class=TasksInfoSerializer)
    # def completed(self, request):
    #     tasks = Task.objects.filter(status=True)
    #     return Response(TasksInfoSerializer(tasks, many=True).data)

    @method_decorator(cache_page(60))
    @action(methods=['GET'], detail=False, serializer_class=TaskSerializer, url_path='top-20')
    def top_20(self, request):
        tasks = Task.objects.filter(
            timelog__end_time__gte=timezone.now() - timedelta(days=30)
        ).annotate(
            work_time=Sum(F('timelog__end_time') - F('timelog__start_time'))
        ).order_by('-work_time')[:20]
        return Response(TaskSerializer(tasks, many=True).data)

    @action(methods=['PATCH'], detail=True, serializer_class=TaskUpdateSerializer, url_path="update-owner")
    def update_owner(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        serializer = TaskUpdateSerializer(instance=task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subject = 'A new task was assigned to you!'
        message = 'Hello, ' + task.owner.last_name + '\n' + task.title + ' was assigned to you. Go and check it out!'
        to_email = task.owner.email
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [to_email])

        return Response({"success": True, "message": "owner updated successfully"})

    @action(methods=['PATCH'], detail=True, serializer_class=TaskUpdateStatusSerializer, url_path="update-status")
    def update_status(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        serializer = TaskUpdateStatusSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        task_completed = validated_data.get('status')
        serializer.save()
        if task.comment_set.exists():
            if task_completed is True:
                subject = 'One of your commented task has been completed!'
                message = 'Hello, ' + task.owner.last_name + '\n' + task.title + ' is done. Congratulations!'
                to_email = task.owner.email
                send_mail(subject, message, DEFAULT_FROM_EMAIL, [to_email])

        return Response({"success": True, "message": "status updated successfully"})


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

    def create(self, request, *args, **kwargs):
        serializer = CommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        task_id = validated_data.get('task')
        com_text = validated_data.get('text')
        self.perform_create(serializer)
        subject = 'One of your tasks was commented!'
        message = 'Hello, ' + task_id.owner.last_name + ', a new comment was posted to your ' + \
                  task_id.title + '\n Comment: "' + com_text + ' "'
        to_email = task_id.owner.email
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [to_email])

        return Response({"success": True, "message": "comment added successfully"})


class UserListView(GenericAPIView):
    serializer_class = GetUsersSerializer

    def get(self, request):
        users = User.objects.all()
        return Response(GetUsersSerializer(users, many=True).data)


class TaskItemView(GenericAPIView):
    serializer_class = TaskItemSerializer
    queryset = Task.objects.all()

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        return Response(TaskItemSerializer(task).data)


class TaskItemLogsView(GenericAPIView):
    serializer_class = TaskItemLogsSerializer
    queryset = Task.objects.all()

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        return Response(TaskItemLogsSerializer(task).data)


class TaskListViewWithWorktime(GenericAPIView):
    serializer_class = TaskItemLogsSerializer
    queryset = Task.objects.all()

    def get(self, request, pk):
        task = Task.objects.all()
        return Response(TaskItemLogsSerializer(task).data)


class TaskSearchView(generics.ListAPIView):
    serializer_class = TaskSearchSerializer
    queryset = Task.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
