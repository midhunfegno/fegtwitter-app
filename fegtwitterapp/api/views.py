from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fegtwitterapp.api.serializers import UserRegisterSerializer, HomeTweetSerializer, UserTweetPostSerializer
from fegtwitterapp.models import UserTweet
from rest_framework import status, generics


class HomeTweetGenericListView(generics.ListCreateAPIView):
    queryset = UserTweet.objects.all()
    serializer_class = HomeTweetSerializer

    def list(self, request, *args, **kwargs):
        currentuser = list(self.request.user.followers.all())
        currentuser.append(self.request.user)
        print("user", currentuser)
        usertweet = UserTweet.objects.filter(user__in=currentuser).all().order_by('-upload_date')
        page = self.paginate_queryset(usertweet)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(usertweet, many=True)
        return Response(serializer.data)


class UserTweetGenericListView(generics.ListAPIView):
    queryset = UserTweet.objects.all()
    serializer_class = HomeTweetSerializer

    def list(self, request, *args, **kwargs):
        currentuser = self.request.user
        print(currentuser)
        usertweet = UserTweet.objects.filter(user=currentuser).all().order_by('-upload_date')
        page = self.paginate_queryset(usertweet)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(usertweet, many=True)
        return Response(serializer.data)


class UserRegistrationApiView(APIView):
    def post(self, request):
        print("UserRegistration", request.data)
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'registered'
            data['fullname'] = account.fullname
            data['email'] = account.email
            data['username'] = account.username
            data['password'] = account.password
            token = Token.objects.create(user=account)
            data['token'] = token.key
            print("Token:", token)
        else:
            data = serializer.errors
        return Response(data)


class UserTweetPostApiView(APIView):
    def post(self, request):
        print("TweetCreate", request.data)
        serializer = UserTweetPostSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            postdata=serializer.save()
            data['text'] = postdata.text
            data['user'] = self.request.user
        else:
            data = serializer.errors
        return Response(data)


class UserHomepageApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        content = {'user': str(request.user), 'userid': str(request.user.id)}
        return Response(content)


class TweetDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTweet.objects.all()
    serializer_class = HomeTweetSerializer





