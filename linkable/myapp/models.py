from django.contrib.auth.hashers import is_password_usable, make_password
from django.contrib.postgres.fields import ArrayField
from django.core.validators import URLValidator
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .manager import MyUserManager


class Recommend(models.Model):
    books = ArrayField(models.IntegerField(), size=20, blank=True,default=list)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("id",)

class Book(models.Model):
    title = models.CharField(max_length=500)
    node = models.IntegerField()
    autor = models.CharField(max_length=500)
    location = models.CharField(max_length=200)
    sellnum = models.IntegerField()
    description = models.TextField()
    imagesource = models.TextField(validators=[URLValidator],default='http://image.yes24.com/momo/TopCate1833/MidCate006/183255693.jpg')

    class Meta:
        ordering = ("id",)

class MyUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='이메일')
    name = models.CharField(max_length=20, verbose_name='이름')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')

    REQUIRED_FIELDS = ['name','email']

    objects = MyUserManager()

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '유저들'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def password_hashing(instance, **kwargs):
    if not is_password_usable(instance.password):
        instance.password = make_password(instance.password)