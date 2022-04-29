from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponse

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from fegtwitterapp.forms import RegistrationForm, PostForm, UpdatePostForm
from fegtwitterapp.models import User, UserTweet


class HomePage(LoginRequiredMixin, ListView):
    model = UserTweet
    queryset = UserTweet.objects.all()
    paginate_by = 10
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # import pdb;pdb.set_trace()
        print("current_user", self.request.user)

        user_timeline_key = "{}_USER_TIMELINE".format(self.request.user)
        user_timeline = cache.get(user_timeline_key)
        print("user_timeline_key", user_timeline_key, user_timeline)

        # import pdb;pdb.set_trace()
        result = []
        if user_timeline is not None:
            new_timeline = sorted(user_timeline, reverse=True)
            for tweet_id in new_timeline:
                result.append(cache.get(f'{tweet_id}_TWEET_ID'))
        context['tweets'] = result
        # print("value:", new_timeline)
        print("usertimeline:", result)

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
        setting up cache for tweets posted by users       
        """
        post_key = f'{post_instance.id}_TWEET_ID'
        cache.set(post_key, {
            "user": post_instance.user,
            "text": post_instance.text,
            "upload_date": post_instance.upload_date
        })
        print("post_key:", post_key)
        print("cached post_key:", cache.get(post_key))

        """             
        setting up cache for user timeline 
        """

        followuser = self.request.user.followers.all().values_list('username', flat=True)
        userkey = [f'{post_instance.user}_USER_TIMELINE']
        print("followuser", followuser)
        userfollowtimeline = cache.get(userkey)
        """
                setting cache for user
        """
        if userfollowtimeline is None:
            userfollowtimeline = []
            print("test_data", userfollowtimeline)
            cache.set(userkey, userfollowtimeline)
        else:
            userfollowtimeline.append(post_instance.id)
            cache.set(userkey, userfollowtimeline)
        print("current user  cache", userfollowtimeline, userkey, cache.get(userkey))
        """
                setting cache for followers
        """
        for followid in followuser:
            followkey = [f'{followid}_USER_TIMELINE']
            followtimeline = cache.get(followkey)
            if followtimeline is None:
                followtimeline = []
                cache.set(followkey, followtimeline)
                print("current follow cache", followtimeline, followkey)
            else:
                followtimeline.append(post_instance.id)
                print("{}".format(followkey), followtimeline)
                cache.set(followkey, followtimeline)
                print("current follow cache", followtimeline, followkey, cache.get(followkey))

        # redis_cache = caches.create_connection('default')
        # redis_cache.get_many(['follow_id1', 'follow_id2', 'follow_id3'])
        # redis_cache.get_many(['follow_id1', 'follow_id2', 'follow_id3'])
        # redis_cache.set_many()

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

    def get_queryset(self):
        return UserTweet.objects.all().filter(user=self.request.user).select_related("user").order_by('-upload_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        Relation_table = User.followers.through
        """        alreadyfollowing is a list that shows users that are already follwing me               """
        alreadyfollowing = Relation_table.objects.filter(to_user=self.request.user).values_list('from_user')
        context['follow_recommendations'] = User.objects.exclude(id__in=alreadyfollowing).order_by('?')[:8]
        return context


class MyTweetUpdateView(LoginRequiredMixin, UpdateView):
    model = UserTweet
    template_name = "mytweetpageupdate.html"
    form_class = UpdatePostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(MyTweetUpdateView, self).form_valid(form=form)

    def get_success_url(self):
        return reverse('my_tweets')


class MyTweetDeleteView(DeleteView):
    model = UserTweet
    template_name = "mytweetpage.html"
    success_url = '/mytweet'

    """       here we use get method and return deleted result         """

    def get(self, request, *args, **kwargs):
        return super(MyTweetDeleteView, self).delete(request, *args)


@csrf_exempt
def ajax_submission(request):

    if request.method == "POST":
        followerid = request.POST.get('element')
        User.objects.get(id=followerid).followers.add(request.user.id)
    return HttpResponse("Ok")


class MyFollowersListView(ListView):
    model = User
    template_name = "followingpage.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        Relation_table = User.followers.through

        """      alreadyfollowing is a list that shows users that are already follwing me         """

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
