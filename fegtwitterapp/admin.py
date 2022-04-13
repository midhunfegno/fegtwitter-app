from django.contrib import admin

# Register your models here.
from fegtwitterapp.models import User_Tweet, Followers, Twitter_User

admin.site.register(Twitter_User)
admin.site.register(Followers)
admin.site.register(User_Tweet)
