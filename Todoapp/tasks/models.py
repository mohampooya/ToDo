from django.db import models
from django.contrib.auth.models import User
#from .models import UserProfile
from django.utils.timezone import now

class TaskList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(default=now) 

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')


    def __str__(self):
        return self.title


from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()

from django.db.models.signals import post_save
from django.dispatch import receiver



class Document(models.Model):
    uploaded_file = models.FileField(upload_to='documents/')


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

