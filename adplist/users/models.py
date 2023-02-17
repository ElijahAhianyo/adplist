from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import CharField
from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import CharField, DateField, EmailField, Model, BooleanField
from django.db import models
from adplist.base.models import TimeStampedModel
from adplist.users.managers import CustomUserManager


class Expertise(TimeStampedModel):
    name = CharField(max_length=30)
    description = CharField(max_length=30)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Default custom user model for ADPList.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    username = None
    USERNAME_FIELD = "email"
    first_name = CharField(max_length=30, null=True)  # type: ignore
    last_name = CharField(max_length=30, null=True)  # type: ignore
    email = EmailField(_("user email"), unique=True)
    location = CharField(max_length=30, null=True)
    title = CharField(max_length=30, null=True)
    employer = CharField(max_length=30, null=True)
    expertise = models.ManyToManyField(Expertise)
    is_member = BooleanField(default=False)
    is_mentor = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        print(f"args| {args}, kwargs: {kwargs}")
        return super().save(*args, **kwargs)
