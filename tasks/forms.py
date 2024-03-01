from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from .templatetags import translations

class BackgroundForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['background']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label=translations.translate_to_persian("email"))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = translations.translate_to_persian('username')
        self.fields['password1'].label = translations.translate_to_persian('password1')
        self.fields['password2'].label = translations.translate_to_persian('password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    background_choices = [
        
        ('custom', 'Upload Custom Background'),
    ]
    background_choice = forms.ChoiceField(choices=background_choices, required=False, label="پس‌زمینه داشبورد")
    custom_background = forms.ImageField(required=False, label="یا بارگذاری پس‌زمینه")

    class Meta:
        model = UserProfile
        fields = [ 'profile_picture', 'background']
    def save(self, *args, **kwargs):
        user = super(CombinedUserProfileForm, self).save(*args, **kwargs)
        user_profile = self.instance
        user_profile.user.first_name = self.cleaned_data['first_name']
        user_profile.user.last_name = self.cleaned_data['last_name']
        user_profile.user.email = self.cleaned_data['email']
        user_profile.user.save()
        return user_profile

        
class CombinedUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    background_choices = [
        ('custom', 'Upload Custom Background'),
    ]
    background_choice = forms.ChoiceField(choices=background_choices, required=False, label="پس‌زمینه داشبورد")
    custom_background = forms.ImageField(required=False, label="یا بارگذاری پس‌زمینه")
    

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
