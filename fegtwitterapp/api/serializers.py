
from rest_framework import serializers


from fegtwitterapp.models import UserTweet
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'username']


class HomeTweetSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        queryset = User.objects.filter(id=instance.user_id)
        return UserRegisterSerializer(queryset, many=True, read_only=True).data

    class Meta:
        model = UserTweet
        fields = ['id', 'user', 'text', 'upload_date']
