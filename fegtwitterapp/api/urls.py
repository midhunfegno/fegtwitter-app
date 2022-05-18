from django.db import router
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from fegtwitterapp.api import views
from fegtwitterapp.api.views import PostTweetViewSet, UserTweetGenericListView, HomeTweetGenericListView, api_root

post_tweets = PostTweetViewSet.as_view({'post': 'create'})

router = DefaultRouter()
router.register("posttweets", PostTweetViewSet, basename="usertweet")

urlpatterns = [
    path('', include(router.urls)),
    path('api/', api_root),
    path('api/userregistration/', views.UserRegistrationApiView.as_view(), name='user_reg'),
    path('api/userlogin/', obtain_auth_token, name='user_login'),
    path('api/userhomepage/', views.UserHomepageApiView.as_view(), name='user_homepage'),
    path('api/hometweets/', views.HomeTweetGenericListView.as_view(), name='hometweets'),
    path('api/usertweets/', views.UserTweetGenericListView.as_view(), name='usertweets'),
    path('api/post_tweets/', post_tweets, name='post-tweets'),
    path('api/usertweets/<int:pk>/', views.TweetDetailGenericView.as_view(), name='user_tweets_manage'),
]
