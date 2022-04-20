from django.urls import path
from django.contrib.auth import views as auth_views
from fegtwitterapp import views

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='homepage'),
    path('', auth_views.LoginView.as_view(), name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_view'),
    path('save/', views.UserTweetCreateView.as_view(), name='tweet_save'),
    path('mytweet/', views.MyTweetListView.as_view(), name='my_tweets'),
    path('mytweetupdate/<int:pk>/', views.MyTweetUpdateView.as_view(), name='my_tweets_update'),
    path('mytweetdelete/<int:pk>/', views.MyTweetDeleteView.as_view(), name='my_tweets_delete'),
    path('reg/', views.UserRegistration.as_view(), name='user_registration'),

]
