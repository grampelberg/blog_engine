from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        'date published', auto_now=True)
    slug = models.SlugField(primary_key=True)
    body = models.TextField()
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('pub_date', 'author')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar', blank=True)

class UserProfileForm(forms.ModelForm):
    class Meta:
        exclude = ('user', )
        model = UserProfile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
