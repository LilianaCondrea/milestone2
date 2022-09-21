from rest_framework import serializers

from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class GetUsersSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ('id', 'full_name')


class UserLogtime(serializers.ModelSerializer):
    user_work_time = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "user_work_time")

    def get_user_work_time(self, obj):
        if obj.user_work_time:
            return obj.user_work_time / 60
        return obj.user_work_time
