from datetime import timedelta

from .models import User
from .serializers import GetUsersSerializer, UserLogtime
from .serializers import UserDetailSerializer
from django.db.models import Sum, F, Q
from django.utils import timezone
from drf_util.decorators import serialize_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterView(GenericAPIView):
    @swagger_auto_schema(request_body=UserDetailSerializer)
    @serialize_decorator(UserDetailSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['email'],
            email=validated_data['email'],
            is_superuser=False,
            is_staff=False
        )
        user.set_password(validated_data['password'])
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class UsersListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = GetUsersSerializer(users, many=True)
        return Response(serializer.data)


# class UserLogtimeView(GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserLogtime
#
#     def get(self, request):
#         users = User.objects.filter(email=self.request.user).annotate(
#             user_work_time=Sum(F('timelog__end_timer') - F('timelog__start_timer'),
#                                filter=Q(timelog__end_timer__gte=timezone.now() - timedelta(days=30))
#                                )
#         )
#         return Response(UserLogtime().data)
