
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Beautiful API",
        default_version='v1',
        description="Hello :)",

    ),
    validators=['ssv'],
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('auth/', include("apps.users.urls")),
    path('', include('apps.tasks.urls')),
]
