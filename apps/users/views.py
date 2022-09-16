from apps.tasks.models import User
from apps.users.serializers import GetUsersSerializer
from apps.users.serializers import UserDetailSerializer
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
