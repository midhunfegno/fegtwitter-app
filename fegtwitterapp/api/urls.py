from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from fegtwitterapp.api import views


urlpatterns = [
    path('api/userregistration/', views.UserRegistrationApiView.as_view(), name='user_reg'),
    path('api/userlogin/', obtain_auth_token, name='user_login'),
    path('api/userhomepage/', views.UserHomepageApiView.as_view(), name='user_homepage'),
    path('api/hometweets/', views.HomeTweetGenericListView.as_view(), name='hometweets'),
    path('api/usertweets/', views.UserTweetGenericListView.as_view(), name='user_tweets'),
    path('api/posttweets/', views.UserTweetPostApiView.as_view(), name='user_tweet_post'),
    path('api/usertweets/<int:pk>/', views.TweetDetailGenericView.as_view(), name='user_tweets_manage'),
]
