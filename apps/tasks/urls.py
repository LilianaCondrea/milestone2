from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet, TaskViewSet, UserListView, TaskSearchView, TaskItemView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='Tasks')
router.register(r'comments', CommentsViewSet, basename='Comments')
urlpatterns = router.urls

urlpatterns = [
                  path('users/', UserListView.as_view(), name='users-list'),
                  path('tasks/search/', TaskSearchView.as_view(), name='task-search'),
                  path('tasks/<int:pk>/comments/', TaskItemView.as_view(), name='task-comments'),
              ] + router.urls
