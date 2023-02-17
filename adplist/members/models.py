from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from adplist.base.models import TimeStampedModel

user = get_user_model()


class Member(TimeStampedModel):
    user = models.ForeignKey(user, related_name="+", on_delete=models.CASCADE)
