from django.contrib import admin

# Register your models here.
from fegtwitterapp.models import UserTweet, User

admin.site.register(User)
admin.site.register(UserTweet)
