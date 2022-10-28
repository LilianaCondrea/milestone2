from .views import HealthView, ProtectedTestView
from django.urls import path

urlpatterns = [
    path("health", HealthView.as_view(), name='health_view'),
    path("protected", ProtectedTestView.as_view(), name='protected_view'),
]
