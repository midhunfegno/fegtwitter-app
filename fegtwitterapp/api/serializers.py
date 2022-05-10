
from rest_framework import serializers


from fegtwitterapp.models import UserTweet
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'username', 'password']


class UserTweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTweet
        fields = ['id', 'user', 'text', 'upload_date']
