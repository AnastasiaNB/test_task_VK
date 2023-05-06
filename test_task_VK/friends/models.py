from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Status(models.Model):
    status = models.CharField(max_length=10)

class FriendRequest(models.Model):
    user_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requests_from'
    )
    user_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requests_to'
    )
    status =  models.ForeignKey(
        Status,
        on_delete=models.SET_DEFAULT,
        default=0
    )

    class Meta:
        unique_together = ['user_from', 'user_to']

