from rest_framework import routers

from fegtwitterapp.api.views import UserTweetViewSet, HomeTweetViewSet, UserRegistrationApiView
from fegtwitterapp.models import UserTweet

router = routers.DefaultRouter()
router.register('hometweets', HomeTweetViewSet, basename='homeTweet')
router.register('usertweets', UserTweetViewSet, basename='userTweet')
# router.register('userregistration', UserRegistrationApiView, basename='User')
