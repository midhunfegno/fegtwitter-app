
# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView

from fegtwitterapp.models import Twitter_User


class homepage(TemplateView):
    template_name = "index.html"


class user_login(TemplateView):
    template_name = "login.html"


class user_registration(CreateView):
    model = Twitter_User
    template_name = "register.html"
    fields = ('fullname', 'username', 'password')
