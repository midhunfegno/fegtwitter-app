
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, related_name='following')
    fullname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    follower_count = models.IntegerField(default=0, blank=True, null=True)
    following_count = models.IntegerField(default=0, blank=True, null=True)
    tweet_count = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.username


class UserTweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                             related_name='tweetusers')
    text = models.CharField(max_length=100, blank=True, null=True)
    """
    date field is set to store current date and time
    upload_date is created date of the user tweet
    """
    upload_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-upload_date']
