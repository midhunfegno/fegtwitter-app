from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache, caches
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from fegtwitterapp.forms import RegistrationForm, PostForm, UpdatePostForm
from fegtwitterapp.models import User, UserTweet


HOME_TIMELINE = '{}_HOME_TIMELINE'
USER_TIMELINE = '{}_USER_TIMELINE'
TWEET_CACHE = '{}_TWEET_ID'
FOLLOWER_CACHE = '{}_FOLLOWER_ID'


class HomePage(LoginRequiredMixin, ListView):
    model = UserTweet
    queryset = UserTweet.objects.all()
    template_name = "index.html"
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        """
        getting dictionary values from the tweetlist
        ------------------------------------------------------------------------------------------------------
        eg:
        TweetList {'671_TWEET_ID': {'id': 671, 'user': <User: midhunmanoj>, 'text': 'ccccccccccccccccccccc',
                        'upload_date': datetime.datetime(2022, 5, 4, 13, 0, 47, 870640, tzinfo=<UTC>)},.....]

        final_result will be as follows
        ------------------------------------------------------------------------------------------------------
        final_result [{'id': 671, 'user': <User: midhunmanoj>, 'text': 'ccccccccccccccccccccc',
         'upload_date': datetime.datetime(2022, 5, 4, 13, 0, 47, 870640, tzinfo=<UTC>)},....]
        """
        context = super().get_context_data(*args, **kwargs)
        home_timeline_key = HOME_TIMELINE.format(self.request.user.username)
        home_timeline = cache.get(home_timeline_key)
        result = []
        redis_cache = caches.create_connection('default')
        if home_timeline is not None:
            new_timeline = sorted(home_timeline, reverse=True)
            for tweet_id in new_timeline:
                result.append(f'{tweet_id}_TWEET_ID')
            """
            Instead of cache.get we use cache.get_many() to reduce data access time from redis cache and with less code
            """
            page_size_limit = 10
            page = int(self.request.GET.get('page', '1'))
            final_result1 = []
            start = ((page - 1) * page_size_limit)
            end = page * page_size_limit
            paginated_result = result[start:end]
            # print("paginated_result", paginated_result)
            tweet_list1 = redis_cache.get_many(paginated_result)
            for key, value in tweet_list1.items():
                final_result1.append(value)
            context['mytweets'] = final_result1

        """
        code for obtaining non followers list
        """
        Relation_table = User.followers.through
        alreadyfollowing = Relation_table.objects.filter(to_user=self.request.user).values_list('from_user', flat=True)
        context['follow_recommendations'] = User.objects.exclude(id__in=alreadyfollowing).order_by('?')[:12]
        return context


class UserRegistration(SuccessMessageMixin, CreateView):
    model = User
    template_name = "register.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        return super(UserRegistration, self).form_valid(form=form)

    def form_invalid(self, form):
        messages.error(self.request, "There are some errors in the form! Please correct the errors and resubmit")
        return super(UserRegistration, self).form_invalid(form=form)

    def get_success_url(self):
        return reverse('login_view')


class UserTweetCreateView(LoginRequiredMixin, CreateView):
    model = UserTweet
    template_name = "index.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        post_instance = form.instance
        """
        setting up cache for tweets posted by users   (each tweets posted)    
        """
        post_key = f'{post_instance.id}_TWEET_ID'
        cache.set(post_key, {
            "id": post_instance.id,
            "user": post_instance.user,
            "text": post_instance.text,
            "upload_date": post_instance.upload_date
        })
        """             
        setting up cache for home timeline (those whom i follow and my tweets )
        """
        follow_user = self.request.user.followers.all().values_list('username', flat=True)
        homeuser_key = HOME_TIMELINE.format(post_instance.user.username)
        homeuser_follow_timeline = cache.get(homeuser_key, default=[])
        homeuser_follow_timeline.append(post_instance.id)
        cache.set(homeuser_key, homeuser_follow_timeline)
        """             
        setting up cache for user timeline (contains only my posts)
        """
        user_key = USER_TIMELINE.format(post_instance.user.username)
        user_follow_timeline = cache.get(user_key, default=[])
        user_follow_timeline.append(post_instance.id)
        cache.set(user_key, user_follow_timeline)
        # print("User Timeline cache", cache.get(user_key))
        """ 
        setting cache for following users (appends each post to followers hometimeline)
        """

        for followid in follow_user:
            follow_key = HOME_TIMELINE.format(followid)
            followtimeline = cache.get(follow_key)
            if followtimeline is None:
                followtimeline = []
            followtimeline.append(post_instance.id)
            cache.set(follow_key, followtimeline)
            # print("current follow cache", followtimeline, follow_key)

        return super(UserTweetCreateView, self).form_valid(form=form)

    def form_invalid(self, form):
        messages.error(self.request, "There are some errors in the form! Please correct the errors and resubmit")
        return super(UserTweetCreateView, self).form_invalid(form=form)

    def get_success_url(self):
        return reverse('homepage')


class MyTweetListView(LoginRequiredMixin, ListView):
    model = UserTweet
    paginate_by = 10
    template_name = "mytweetpage.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_timeline_key = USER_TIMELINE.format(self.request.user.username)
        user_timeline = cache.get(user_timeline_key)
        myresult = []
        """
        Sorting the result obtained
        """
        redis_cache = caches.create_connection('default')
        if user_timeline is not None:
            new_timeline = sorted(user_timeline, reverse=True)
            for tweet_id in new_timeline:
                myresult.append(f'{tweet_id}_TWEET_ID')
            """
            Instead of cache.get we use cache.get_many() to reduce data access time from redis cache and with less code
            """
            page_size_limit = 10
            page = int(self.request.GET.get('page', '1'))
            myfinal_result = []
            start = ((page - 1) * page_size_limit)
            end = page * page_size_limit
            paginated_result = myresult[start:end]
            # print("paginated_result", paginated_result)
            tweet_list = redis_cache.get_many(paginated_result)
            for key, value in tweet_list.items():
                myfinal_result.append(value)
            context['mytweetss'] = myfinal_result
        """       
        Displaying non follower list
        """
        Relation_table = User.followers.through
        alreadyfollowing = Relation_table.objects.filter(to_user=self.request.user).values_list('from_user')
        context['follow_recommendations'] = User.objects.exclude(id__in=alreadyfollowing).order_by('?')[:12]
        return context


class MyTweetUpdateView(LoginRequiredMixin, UpdateView):
    model = UserTweet
    template_name = "mytweetpageupdate.html"
    form_class = UpdatePostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        post_instance = form.instance

        old_tweet_id = self.kwargs.get('pk')
        # print("old_tweet id", old_tweet_id)
        """
        deleting the existing post
        """
        cache.delete(TWEET_CACHE.format(old_tweet_id))
        """
        setting up cache for updating tweets    
        """
        update_tweet_key = TWEET_CACHE.format(post_instance.id)
        # print("update_tweet id", update_tweet_key)
        cache.set(update_tweet_key, {
            "id": post_instance.id,
            "user": post_instance.user,
            "text": post_instance.text,
            "upload_date": post_instance.upload_date
        })
        # print("update cache:", cache.get(update_tweet_key))
        """
        removing old data cache and updating new cache data 
        """
        follow_user = self.request.user.followers.all().values_list('username', flat=True)

        for followid in follow_user:
            follow_key = HOME_TIMELINE.format(followid)
            followtimeline = cache.get(follow_key)
            for tid in followtimeline:
                followtimeline.remove(tid)
                followtimeline.append(post_instance.id)
            cache.set(follow_key, followtimeline)
            # print("current follow cache", followtimeline, follow_key, cache.get(follow_key))
        # print("update cache:", cache.get(update_tweet_key))
        return super(MyTweetUpdateView, self).form_valid(form=form)

    def get_success_url(self):
        return reverse('my_tweets')


class MyTweetDeleteView(LoginRequiredMixin, DeleteView):
    model = UserTweet
    template_name = "mytweetpage.html"
    success_url = '/mytweet'

    """
    here we use get method and return deleted result
    """
    def get(self, request, *args, **kwargs):
        currentuser = self.request.user.username
        update_tweet_id = self.kwargs.get('pk')
        userpost = cache.get(USER_TIMELINE.format(currentuser))
        userhomepost = cache.get(HOME_TIMELINE.format(currentuser))
        """
        deleting tweet from user timeline
        """
        for pid in userpost:
            if pid == update_tweet_id:
                userpost.remove(pid)
        """
        deleting tweet from home timeline
        """
        for pid in userhomepost:
            if pid == update_tweet_id:
                userhomepost.remove(pid)
        cache.delete(TWEET_CACHE.format(update_tweet_id))
        return super(MyTweetDeleteView, self).delete(request, *args)


@csrf_exempt
def ajax_submission(request):
    if request.method == "POST":
        followerid = request.POST.get('element')
        User.objects.get(id=followerid).followers.add(request.user.id)
    return HttpResponse("Ok")


class MyFollowersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "followingpage.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        Relation_table = User.followers.through
        """
        alreadyfollowing is a list that shows users that are already follwing me
        """
        alreadyfollowing = Relation_table.objects.filter(to_user=self.request.user).values_list('from_user', flat=True)
        context['follow_recommendations'] = User.objects.exclude(id__in=alreadyfollowing)
        context['alreadyfollowing'] = User.objects.get(id=self.request.user.id).followers.all()
        return context


@csrf_exempt
def ajax_submission_unfollow(request):
    if request.method == "POST":
        followerid = request.POST.get('element')
        User.objects.get(id=followerid).followers.remove(request.user.id)
        return HttpResponse("Ok")
