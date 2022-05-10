
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fegtwitterapp.api.serializers import UserTweetSerializer, UserRegisterSerializer
from fegtwitterapp.models import UserTweet
from rest_framework import viewsets, status


class HomeTweetViewSet(viewsets.ViewSet):
    queryset = UserTweet.objects.all()
    serializer_class = UserTweetSerializer

    def list(self, request):
        currentuser = list(self.request.user.followers.all())
        currentuser.append(self.request.user)
        print("user", currentuser)
        usertweet = UserTweet.objects.filter(user__in=currentuser).all().order_by('-upload_date')
        serializer = UserTweetSerializer(usertweet, many=True)
        return Response(serializer.data)

    def create(self, request):
        print("TweetCreate", request.data)
        serializer = UserTweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        tweetid = self.get_object(pk)
        serializer = UserTweetSerializer(tweetid)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTweetViewSet(viewsets.ViewSet):
    queryset = UserTweet.objects.all()
    serializer_class = UserTweetSerializer

    def list(self, request):
        currentuser = self.request.user
        print(currentuser)
        usertweet = UserTweet.objects.filter(user=currentuser).all().order_by('-upload_date')
        serializer = UserTweetSerializer(usertweet, many=True)
        return Response(serializer.data)


class UserRegistrationApiView(APIView):
    def post(self, request):
        print("UserRegistration", request.data)
        serializer = UserRegisterSerializer(data=request.data)
        # for user in User.objects.all():
        #     Token.objects.get_or_create(user=user)
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


class UserHomepageApiView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        content = {'user': str(request.user), 'userid': str(request.user.id)}
        return Response(content)

