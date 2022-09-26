from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet, TaskViewSet, UserListView, TaskItemView, TaskItemLogsView
from ..timelogs.views import TimeLogViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='Tasks')
router.register(r'timelogs', TimeLogViewSet, basename='timelogs')
router.register(r'comments', CommentsViewSet, basename='Comments')
# urlpatterns = router.urls

urlpatterns = [
                  path('users/', UserListView.as_view(), name='users-list'),
                  # path('tasks/search/', TaskSearchView.as_view(), name='task-search'),
                  # path('users/logtime/', UserLogtimeView.as_view(), name='user_logtime'),
                  path('tasks/<int:pk>/comments/', TaskItemView.as_view(), name='task-comments'),
                  path('tasks/<int:pk>/logs/', TaskItemLogsView.as_view(), name='task-logs'),
              ] + router.urls
