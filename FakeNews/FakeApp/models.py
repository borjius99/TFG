import random
import string

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

import jsonfield


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, org_name, org_source, wallet, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, org_name=org_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, org_name, org_source, wallet, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, org_name, org_source, wallet, password, **other_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    orgId = models.IntegerField(unique=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    org_name = models.CharField(max_length=100, unique=True)
    org_source = models.CharField(max_length=100, default='')
    wallet = models.CharField(max_length=100, unique=True)
    reputation = models.IntegerField(default=0)
    canPublish = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['org_name', 'org_source', 'wallet']

    def __str__(self):
        return f'{self.org_name}'


def voters_default():
    return {"voters": []}


class News(models.Model):
    newsId = models.IntegerField(unique=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    url = models.URLField(max_length=200, default='')
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    votosPositivos = models.IntegerField(default=0)
    votosNegativos = models.IntegerField(default=0)
    voters = models.JSONField(default='{}')
    legitima = models.BooleanField(default=True)
    visualizations = models.IntegerField(default=0)

    def __str__(self):
        return self.title
