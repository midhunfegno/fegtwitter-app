
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, null=True, related_name='following')
    fullname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    follower_count = models.IntegerField(default=0, blank=True, null=True)
    following_count = models.IntegerField(default=0, blank=True, null=True)
    tweet_count = models.IntegerField(default=0, blank=True, null=True)
    # followers = models.ManyToManyField('self', blank=True, through='user.Twitter_User',\
    # through_fields=('user', 'follow'))

    def __str__(self):
        return self.username


class UserTweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    """date field is set to store current date and time"""
    upload_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-upload_date']


# class Follower(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     follow = models.ForeignKey(User, on_delete=models.CASCADE)
#     """
#     follow_id used for identifying the follower user id
#     """


# class Twitter_User(models.Model):
#     fullname = models.CharField(max_length=100, blank=True, null=True)
#     username = models.CharField(max_length=100, blank=True, null=True)
#     email = models.CharField(max_length=100, blank=True, null=True,)
#     password = models.CharField(max_length=100, blank=True)
#     follower_count = models.IntegerField(default=0, blank=True, null=True)
#     following_count = models.IntegerField(default=0, blank=True, null=True)
#     tweet_count = models.IntegerField(default=0, blank=True, null=True)
