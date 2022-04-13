from django.contrib.auth.models import User, AbstractUser
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
    pass


class Followers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    """
    subscription_id used for identifying the follower user id
    """
    subscription_id = models.IntegerField(default=0, blank=True)


class User_Tweet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, blank=True)
