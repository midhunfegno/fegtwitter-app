from django.urls import path

from fegtwitterapp import views

urlpatterns = [
    path('home/', views.homepage.as_view(), name='homepage'),
    path('', views.user_login.as_view(), name='user_login'),
    path('reg/', views.user_registration.as_view(), name='user_registration'),

]