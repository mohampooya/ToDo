from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

        
class CombinedUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

    def save(self, *args, **kwargs):
        user = super(CombinedUserProfileForm, self).save(*args, **kwargs)
        user_profile = self.instance
        user_profile.user.first_name = self.cleaned_data['first_name']
        user_profile.user.last_name = self.cleaned_data['last_name']
        user_profile.user.email = self.cleaned_data['email']
        user_profile.user.save()
        return user_profile

from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'list']
