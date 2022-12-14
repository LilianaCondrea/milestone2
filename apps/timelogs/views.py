from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import TimeLog
from .serializers import TimeLogSerializer, TimeLogStartTimerSerializer, TimeLogEndTimerSerializer


class TimeLogViewSet(ModelViewSet):
    queryset = TimeLog.objects.all()
    serializer_class = TimeLogSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TimeLogSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['post'], detail=False, serializer_class=TimeLogStartTimerSerializer)
    def start(self, request):
        serializer = TimeLogStartTimerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_time = timezone.now()
        serializer.save(start_timer=current_time, owner=self.request.user)
        return Response({"success": True, "message": "timer started"})

    @action(methods=['post'], detail=False, serializer_class=TimeLogEndTimerSerializer)
    def stop(self, request):
        if TimeLog.objects.filter(end_timer__isnull=True):
            last_timelog_list = TimeLog.objects.filter(end_timer__isnull=True).order_by('start_timer').first()
            last_timelog = get_object_or_404(TimeLog.objects.filter(pk=last_timelog_list.pk))
            serializer = TimeLogEndTimerSerializer(instance=last_timelog, data=request.data)
            serializer.is_valid(raise_exception=True)
            current_time = timezone.now()
            serializer.save(end_timer=current_time, owner=self.request.user)
            return Response({"success": True, "message": "timer stopped"})
        return Response({"success": False, "message": "there isn't started log for this task id"})
