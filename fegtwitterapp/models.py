from enum import unique

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# class Twitter_User(models.Model):
#     fullname = models.CharField(max_length=100, blank=True, null=True)
#     username = models.CharField(max_length=100, blank=True, null=True)
#     email = models.CharField(max_length=100, blank=True, null=True,)
#     password = models.CharField(max_length=100, blank=True)
#     follower_count = models.IntegerField(default=0, blank=True, null=True)
#     following_count = models.IntegerField(default=0, blank=True, null=True)
#     tweet_count = models.IntegerField(default=0, blank=True, null=True)

class Twitter_User(AbstractUser):
    user = models.ManyToManyField('self', null=True, blank=True)
    followers = models.ManyToManyField('self', null=True, blank=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    follower_count = models.IntegerField(default=0, blank=True, null=True)
    following_count = models.IntegerField(default=0, blank=True, null=True)
    tweet_count = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.username


# class Followers(models.Model):
#     user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     follow_id = models.ForeignKey(Twitter_User, on_delete=models.CASCADE)
#     """
#     follow_id used for identifying the follower user id
#     """


class User_Tweet(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=100, blank=True, null=True)
