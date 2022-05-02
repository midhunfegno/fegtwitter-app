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
from django.core.cache.backends.base import DEFAULT_TIMEOUT

USER_TIMELINE = '{}_USER_TIMELINE'
TWEET_CACHE = '{}_TWEET_ID'


class HomePage(LoginRequiredMixin, ListView):
    model = UserTweet
    queryset = UserTweet.objects.all()
    paginate_by = 10
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_timeline_key = USER_TIMELINE.format(self.request.user.username)
        user_timeline = cache.get(user_timeline_key)
        print("user_timeline_key", user_timeline_key, user_timeline)
        result = []
        if user_timeline is not None:
            new_timeline = sorted(user_timeline, reverse=True)
            for tweet_id in new_timeline:
                result.append(cache.get(f'{tweet_id}_TWEET_ID'))
        context['tweets'] = result
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
            "id": post_instance.id,
            "user": post_instance.user,
            "text": post_instance.text,
            "upload_date": post_instance.upload_date
        })
        """             
        setting up cache for user timeline 
        """
        follow_user = self.request.user.followers.all().values_list('username', flat=True)
        user_key = USER_TIMELINE.format(post_instance.user.username)
        user_follow_timeline = cache.get(user_key, default=[])
        user_follow_timeline.append(post_instance.id)
        cache.set(user_key, user_follow_timeline)
        import pdb; pdb.set_trace()
        """
        setting cache for followers
        """
        for followid in follow_user:
            follow_key = USER_TIMELINE.format(followid)
            followtimeline = cache.get(follow_key)
            if followtimeline is None:
                followtimeline = []
            followtimeline.append(post_instance.id)
            cache.set(follow_key, followtimeline)
            print("current follow cache", followtimeline, follow_key)
        return super(UserTweetCreateView, self).form_valid(form=form)

        # redis_cache = caches.create_connection('default')
        # redis_cache.get_many(['follow_id1', 'follow_id2', 'follow_id3'])
        # redis_cache.get_many(['follow_id1', 'follow_id2', 'follow_id3'])
        # redis_cache.set_many()

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
