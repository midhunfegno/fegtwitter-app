from django.urls import path
from django.contrib.auth import views as auth_views
from fegtwitterapp import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('login/', auth_views.LoginView.as_view(), name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_view'),
    path('save/', views.UserTweetCreateView.as_view(), name='tweet_save'),
    path('mytweet/', views.MyTweetListView.as_view(), name='my_tweets'),
    path('mytweetupdate/<int:pk>/', views.MyTweetUpdateView.as_view(), name='my_tweets_update'),
    path('mytweetdelete/<int:pk>/', views.MyTweetDeleteView.as_view(), name='my_tweets_delete'),
    path('reg/', views.UserRegistration.as_view(), name='user_registration'),
    path('ajax/', views.ajax_submission, name='ajax_submission'),
    path('ajax_unfollow/', views.ajax_submission_unfollow, name='ajax_submission_unfollow'),
    path('following/', views.MyFollowersListView.as_view(), name='following_users'),

]
