from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, null=True, blank=True) #닉네임
    birthday = models.DateField(null=True, blank=True) #생일
    gender = models.CharField(max_length=10, blank=True) #성별 (생략가능)
    bio = models.TextField(blank=True) #자기소개 (생략가능)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True) #팔로잉 시스템

    def __str__(self):
        return self.username

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()
