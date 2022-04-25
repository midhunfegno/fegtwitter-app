
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from fegtwitterapp.forms import RegistrationForm, PostForm, UpdatePostForm
from fegtwitterapp.models import User, UserTweet


class HomePage(LoginRequiredMixin, ListView):
    model = UserTweet
    paginate_by = 10
    template_name = "index.html"

    def get_queryset(self):
        return UserTweet.objects.all().exclude(user=self.request.user).order_by('-upload_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        Relation_table = User.followers.through
        """
        alreadyfollowing is a list that shows users that are already follwing 
        """
        alreadyfollowing = Relation_table.objects.filter(to_user=self.request.user).values_list('from_user', flat=True)
        context['follow_recommendations'] = User.objects.exclude(id__in=alreadyfollowing)
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
        # import pdb
        # pdb.set_trace()
        form.instance.user = self.request.user
        form.save()
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
        return UserTweet.objects.all().filter(user=self.request.user).order_by('-upload_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        Relation_table = User.followers.through
        """
        alreadyfollowing is a list that shows users that are already follwing me
        """
        alreadyfollowing = Relation_table.objects.filter(to_user=self.request.user).values_list('from_user', flat=True)
        context['follow_recommendations'] = User.objects.exclude(id__in=alreadyfollowing)
        return context


class MyTweetUpdateView(LoginRequiredMixin, UpdateView):
    model = UserTweet
    template_name = "mytweetpageupdate.html"
    form_class = UpdatePostForm

    def form_valid(self, form):
        # form = UpdatePostForm(instance=self.get_object())
        form.instance.user = self.request.user
        form.save()
        return super(MyTweetUpdateView, self).form_valid(form=form)

    def get_success_url(self):

        return reverse('my_tweets')


class MyTweetDeleteView(DeleteView):
    model = UserTweet
    template_name = "mytweetpage.html"
    success_url = '/mytweet'
    """
    here we use get method and return deleted result
    """
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
