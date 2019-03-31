from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=128, null=False)
    nickname = models.CharField(max_length=128, null=False)
    comment = models.TextField(null=True, blank=True)
