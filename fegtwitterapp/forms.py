from django import forms
from django.forms import ModelForm
from fegtwitterapp.models import User, UserTweet


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'email', 'username', 'password']

    def save(self, commit=True):
        password = self.cleaned_data['password']
        self.instance.set_password(password)
        return super(RegistrationForm, self).save(commit=commit)


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'tweetBox', 'id': 'tweetinput',
                                                         "placeholder": "What's happening?"}))

    class Meta:
        model = UserTweet
        fields = ['text']


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = UserTweet
        fields = ['text']
